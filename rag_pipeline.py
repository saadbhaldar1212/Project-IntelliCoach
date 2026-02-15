"""RAG pipeline module for indexing FAQ documents into Azure AI Search.

This module handles downloading FAQ sheets, building documents, creating
and updating semantic search indexes, and uploading documents to Azure AI Search.
"""

import os
from pathlib import Path
import pandas as pd
from openpyxl.utils.exceptions import InvalidFileException

# Azure SDK
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
)
from azure.search.documents import SearchClient

from dotenv import find_dotenv, load_dotenv


from helpers.helper_functions import (
    create_s3_client,
    download_faq_sheet,
    download_secret_key,
)
from settings.config import config


_ = load_dotenv(find_dotenv())


def build_docs_from_excel(excel_path: str):
    """Build document list from Excel FAQ sheet.

    Args:
        excel_path (str): Path to Excel file containing FAQ data.

    Returns:
        list: List of documents with id, question, answer, and content fields.

    Raises:
        RuntimeError: If required Question and Answer columns are not found.
    """
    df = pd.read_excel(excel_path, engine="openpyxl")
    cols = list(df.columns)
    # match question/answer columns (same tolerant logic used in notebook)
    q_candidates = ["Question", "question", "Qustion", "question_text"]
    a_candidates = ["Answer", "answer", "response", "Response"]
    q_col = next((c for c in cols if c in q_candidates), None)
    a_col = next((c for c in cols if c in a_candidates), None)
    if not q_col:
        for c in cols:
            if c.lower() == "question" or c.lower().startswith("quest"):
                q_col = c
                break
    if not a_col:
        for c in cols:
            if c.lower() == "answer" or c.lower().startswith("ans"):
                a_col = c
                break
    if not q_col or not a_col:
        raise RuntimeError(f"Required columns not found. Found columns: {cols}.")

    trimmed = (
        df[[q_col, a_col]]
        .fillna("")
        .rename(columns={q_col: "question", a_col: "answer"})
    )
    docs = []
    for i, row in trimmed.iterrows():
        docs.append(
            {
                "id": str(i + 1),
                "question": str(row["question"]),
                "answer": str(row["answer"]),
                "content": f"{row['question']}\n\n{row['answer']}",
            }
        )
    return docs


def create_or_update_semantic_index(endpoint: str, admin_key: str, index_name: str):
    """Create or update semantic search index in Azure AI Search.

    Args:
        endpoint (str): Azure Search service endpoint.
        admin_key (str): Azure Search admin key.
        index_name (str): Name of the index to create/update.

    Raises:
        RuntimeError: If endpoint or admin_key not set, or index creation fails.
    """
    if not endpoint or not admin_key:
        raise RuntimeError(
            "azure_search_endpoint and azure_search_key must be set in environment"
        )

    credential = AzureKeyCredential(admin_key)
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

    fields = [
        SimpleField(
            name="id", type=SearchFieldDataType.String, key=True, filterable=True
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            analyzer_name="en.microsoft",
        ),
        SearchableField(
            name="question",
            type=SearchFieldDataType.String,
            analyzer_name="en.microsoft",
            sortable=False,
            filterable=False,
        ),
        SearchableField(
            name="answer",
            type=SearchFieldDataType.String,
            analyzer_name="en.microsoft",
            sortable=False,
            filterable=False,
        ),
    ]

    semantic_config = SemanticConfiguration(
        name="default",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="question"),
            content_fields=[SemanticField(field_name="content")],
            keywords_fields=[SemanticField(field_name="answer")],
        ),
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    index = SearchIndex(name=index_name, fields=fields, semantic_search=semantic_search)

    # create or update index
    try:
        index_client.create_or_update_index(index)
        print(f"Index created/updated: {index_name}")
    except AzureError as e:
        raise RuntimeError(f"Failed to create/update index: {e}") from e


def upload_documents_to_index(
    endpoint: str, admin_key: str, index_name: str, documents: list
):
    """Upload documents to Azure AI Search index in batches.

    Args:
        endpoint (str): Azure Search service endpoint.
        admin_key (str): Azure Search admin key.
        index_name (str): Name of the target index.
        documents (list): List of documents to upload.

    Raises:
        AzureError: If document upload fails.
    """
    credential = AzureKeyCredential(admin_key)
    search_client = SearchClient(
        endpoint=endpoint, index_name=index_name, credential=credential
    )

    # upload in batches to avoid E/G limits
    batch_size = 1000
    try:
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            search_client.upload_documents(documents=batch)
            print(f"Uploaded batch {i // batch_size + 1}: {len(batch)} docs")
    except AzureError as e:
        raise RuntimeError(f"Failed to upload documents: {e}") from e


def download_and_index_faq(
    bucket_name: str = config.bucket_name,
    key: str = config.faq_sheet_key,
    local_path: str = config.local_faq_sheet_path,
):
    """Download FAQ sheet and index documents into Azure AI Search.

    Args:
        bucket_name (str): S3 bucket name (default: config.bucket_name).
        key (str): S3 object key (default: config.faq_sheet_key).
        local_path (str): Local file path (default: config.local_faq_sheet_path).
    """
    s3 = create_s3_client()
    print("Downloading FAQ sheet...")
    download_faq_sheet(s3, bucket_name, key, local_path)
    print("FAQ sheet downloaded to", local_path)

    # load into runtime config for app use
    try:
        config.df_excel = pd.read_excel(local_path, engine="openpyxl")
        logger_msg = f"Loaded FAQ sheet into config (rows={len(config.df_excel)})"
        print(logger_msg)
    except InvalidFileException as e:
        print(f"Failed to load FAQ sheet into config: {e}")

    # download secret key (if present) so local env has credentials for Google/AOAI
    try:
        download_secret_key(
            s3, bucket_name, config.secret_auth_key, config.local_secret_key_base
        )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
            Path(config.local_secret_key_base).resolve()
        )
        print("Secret key downloaded and GOOGLE_APPLICATION_CREDENTIALS set.")
    except FileNotFoundError as e:
        print(f"No secret key downloaded or failed: {e}")

    docs = build_docs_from_excel(local_path)
    print(f"Built {len(docs)} documents from FAQ sheet")

    # Create or update semantic index
    create_or_update_semantic_index(
        config.azure_search_endpoint,
        config.azure_search_key,
        config.azure_search_index,
    )

    # Upload documents
    upload_documents_to_index(
        config.azure_search_endpoint,
        config.azure_search_key,
        config.azure_search_index,
        docs,
    )
    print("Indexing complete")


if __name__ == "__main__":
    download_and_index_faq()
