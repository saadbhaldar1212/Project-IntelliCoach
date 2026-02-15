"""Helper functions for fitness chatbot.

This module provides utilities for authentication, text normalization, AI chat
completion, S3 file management, and fitness-related query processing.
"""

import re
import json
import os
import boto3

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from azure.core.exceptions import AzureError
from google.genai import types

from settings.config import config
from settings.logger_setup import logger


x_api_key_header = APIKeyHeader(name="X-API-KEY")


def authenticate(x_api_key: str = Depends(x_api_key_header)):
    """
    Authenticates the provided X-API-KEY against the configured
    authentication key.
    Args:
        x_api_key (str): The X-API-KEY provided in the request header.
    Raises:
        HTTPException: If the provided X-API-KEY does not match the
        configured authentication key, an HTTP 401 Unauthorized
        exception is raised.
    """
    if x_api_key != config.x_api_authentication_key:
        logger.error("Invalid X-API-KEY given during authentication")
        raise HTTPException(status_code=401, detail="Invalid X-API-KEY")


def normalize_text_for_vdb_creation(s):
    """Normalize input text for database creation and similarity matching.

    Performs whitespace collapsing, punctuation removal, and lowercasing
    to produce normalized tokens suitable for comparisons.

    Args:
        s (str): The input text string to be normalized.

    Returns:
        str: The normalized text string.

    Raises:
        RuntimeError: If normalization fails.
    """
    try:
        s = re.sub(r"\s+", " ", s).strip()
        s = re.sub(r".,", "", s)
        s = s.replace("..", ".")
        s = s.replace("..", ".")
        s = s.replace("\n", "")
        s = s.replace("?", "")
        s = s.replace(".", "")
        s = s.strip()
        s = s.lower()
        return s
    except Exception as e:
        raise RuntimeError("Failed to normalize text for VDB creation") from e


def get_chat_completion(system_message, user_message):
    """Generate chat completion using Gemini API.

    Uses Gemini Chat Completion API with system and user messages
    to generate a response.

    Args:
        system_message (str): System instruction for the model.
        user_message (str): User query/message.

    Returns:
        dict: Parsed JSON response from the model.

    Raises:
        Exception: If API call or JSON parsing fails.
    """

    response = config.gemini_client.models.generate_content(
        model=config.llm_name,
        config=types.GenerateContentConfig(
            system_instruction=system_message,
            temperature=config.llm_temperature,
            top_p=config.llm_top_p,
            max_output_tokens=config.llm_max_output_tokens,
        ),
        contents=user_message,
    ).text

    double_curly_match = re.search(r"\{\{(.*?)\}\}", response, re.DOTALL)
    if double_curly_match:
        return json.loads("{" + double_curly_match.group(1) + "}")

    match = re.search(r"\{[^{}]*\}", response, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        return json.loads(response)


def create_s3_client():
    """
    Create and return a boto3 S3 client using configured endpoint and credentials.
    """
    return boto3.client(
        "s3",
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key,
        aws_secret_access_key=config.secret_key,
    )


def ensure_dir(path):
    """Ensure directory exists for given file path.

    Args:
        path (str): File path for which parent directory should exist.
    """
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def download_s3_file(s3, bucket, key, local_path):
    """Download file from S3 bucket to local path.

    Args:
        s3: Boto3 S3 client.
        bucket (str): S3 bucket name.
        key (str): S3 object key.
        local_path (str): Local destination path.
    """
    ensure_dir(local_path)
    logger.info("Downloading %s to %s...", key, local_path)
    s3.download_file(bucket, key, local_path)


def download_faq_sheet(s3, bucket, key, local_path):
    """Download the FAQ sheet from S3 to the specified local path."""
    download_s3_file(s3, bucket, key, local_path)


def download_secret_key(s3, bucket, key, local_path):
    """Download the secret key file from S3 to the specified local path."""
    download_s3_file(s3, bucket, key, local_path)


def download_vdb_directory(s3, bucket, prefix, local_base):
    """Download all files under the given S3 prefix, preserving directory structure."""
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):
                continue
            rel_path = key[len(prefix) :]
            local_path = os.path.join(local_base, rel_path)
            download_s3_file(s3, bucket, key, local_path)


def get_fitness_related_output(query: str, topics: list):
    """Generate fitness-related response based on query and topics.

    Uses AI model to generate fitness-specific answers.

    Args:
        query (str): User's fitness-related query.
        topics (list): List of topics for context.

    Returns:
        str: Generated response from AI model.

    Raises:
        Exception: If response generation fails.
    """

    try:
        response = get_chat_completion(
            system_message=(
                "You are a Fitness Coach Expert who only answer for question "
                "which are related to Fitness, Gym and Health."
            ),
            user_message=(
                f"{config.fitness_prompt.format(query=query, topics=topics)}"
            ),
        )
        return response

    except Exception as e:
        logger.exception(
            "Error in helper_function: get_fitness_related_output: %s", str(e)
        )
        raise e


def is_chit_chat(question):
    """Determine if question is chit-chat or greeting.

    Uses AI model to analyze if the question is casual conversation.

    Args:
        question (str): The question to analyze.

    Returns:
        dict: JSON response with is_greetings_based boolean.

    Raises:
        Exception: If analysis fails.
    """
    try:
        response = get_chat_completion(
            system_message="You are an AI Assistant.",
            user_message=f"{config.is_greetings.format(question=question)}",
        )
        return response
    except Exception as e:
        logger.exception("Error in helper_function: is_chit_chat: %s", str(e))
        raise e


def greet_back():
    """Generate a greeting response.

    Uses AI model to generate a friendly greeting back to the user.

    Returns:
        dict: JSON response with greet_back message.

    Raises:
        Exception: If greeting generation fails.
    """
    try:
        response = get_chat_completion(
            system_message="You are an AI Assistant.",
            user_message=config.greet_back,
        )
        return response
    except Exception as e:
        logger.exception("Error in helper_function: greet_back: %s", str(e))
        raise e


def query_llm(query, topics):
    """Query LLM with fallback to Azure AI Search.

    Attempts to find answer using Azure AI Search semantic ranking,
    falls back to FAQ sheet exact match, and finally uses LLM.

    Args:
        query (str): User's query.
        topics (list): List of topics for context.

    Returns:
        tuple: (source, answer) where source indicates answer origin.

    Raises:
        Exception: If query processing fails.
    """
    try:
        # Use Azure AI Search semantic ranking instead of local VDB similarity
        # Normalize query for consistency with existing logic
        query_norm = normalize_text_for_vdb_creation(query)

        if config.search_client:
            try:
                # Run a semantic query against the configured index
                results = config.search_client.search(
                    search_text=query_norm,
                    query_type="semantic",
                    semantic_configuration_name="default",
                    top=3,
                    select="id,question,answer,content",
                )

                # Evaluate top results using reranker score
                best = None
                best_score = -1.0
                for r in results:
                    reranker = r.get("@search.reranker_score", 0) or 0
                    if reranker > best_score:
                        best_score = reranker
                        best = r

                # If a confident semantic match is found, return it (source: FAQ_AISEARCH)
                # Reranker scores are typically in a 0..4 range; choose a conservative threshold
                if best and best_score >= 1.5:
                    faq_answer = best.get("answer") or best.get("content")
                    source = "FAQ_AISEARCH"
                    logger.info(
                        "Answer from AI Search (reranker_score=%s): %s",
                        best_score,
                        faq_answer,
                    )
                    return source, faq_answer
            except AzureError as e:
                logger.exception("Azure Search query failed: %s", e)

        # If we reach here, fall back to LLM-based responses (greeting detection, fitness prompt)
        # Use existing logic for greetings and LLM output
        # We will use the original doc-based greetings approach on the query text
        is_greetings_based = is_chit_chat(query_norm)["is_greetings_based"]
        if is_greetings_based:
            source = "LLM"
            greet = greet_back()["greet_back"]
            logger.info("Answer from AI Assistant: %s", greet)
            return source, greet
        else:
            source = "LLM"
            fitness_query_output = get_fitness_related_output(
                query=query_norm, topics=topics
            )["answer"]
            properties = {
                "custom_dimensions": {
                    "incoming_query": query_norm,
                    "answer": fitness_query_output,
                    "topics": topics,
                }
            }
            logger.info("fitness_query_output: %s", properties, extra=properties)
            return source, fitness_query_output
    except Exception as e:
        logger.error("Error in query_llm: %s", e)
        raise e
