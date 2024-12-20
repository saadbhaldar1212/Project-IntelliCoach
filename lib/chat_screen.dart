import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'message.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:chat_bubbles/bubbles/bubble_normal.dart';
import 'package:multi_dropdown/multi_dropdown.dart';

import 'package:fitness_advisor_chatbot/components/app_bar.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key, required this.chatScreenTitle});

  final String chatScreenTitle;

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  TextEditingController controller = TextEditingController();
  ScrollController scrollController = ScrollController();
  bool isTyping = false;
  List<Message> msgs = [];
  List<Message> errorMessage = [];

  // TODO: Fetch Topics from Database
  var items = [
    DropdownItem(label: 'Fitness', value: 'Fitness', selected: true),
    DropdownItem(label: 'Health', value: 'Health'),
  ];
  final formKey = GlobalKey<FormState>();
  final multiSelectController = MultiSelectController<String>();
  List<DropdownItem<String>> selectedItems = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MyAppBar(
        title: widget.chatScreenTitle,
      ),
      body: Column(
        children: [
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: SizedBox(
                width: MediaQuery.of(context).size.width,
                child: Form(
                  key: formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.max,
                    children: [
                      const SizedBox(
                        height: 4,
                      ),
                      MultiDropdown<String>(
                        items: items,
                        controller: multiSelectController,
                        enabled: true,
                        searchEnabled: true,
                        autovalidateMode: AutovalidateMode.onUserInteraction,
                        chipDecoration: ChipDecoration(
                          backgroundColor:
                              Theme.of(context).colorScheme.primary,
                          wrap: true,
                          runSpacing: 2,
                          spacing: 10,
                        ),
                        fieldDecoration: FieldDecoration(
                          hintText: 'Topics',
                          hintStyle: TextStyle(
                            color: Theme.of(context).colorScheme.tertiary,
                          ),
                          prefixIcon: const Icon(Icons.menu),
                          showClearIcon: false,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                            borderSide: BorderSide(
                              color: Theme.of(context).colorScheme.tertiary,
                            ),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                            borderSide: BorderSide(
                              color: Theme.of(context).colorScheme.primary,
                            ),
                          ),
                        ),
                        dropdownDecoration: DropdownDecoration(
                          backgroundColor:
                              Theme.of(context).colorScheme.secondary,
                          marginTop: 2,
                          maxHeight: 500,
                          header: const Padding(
                            padding: EdgeInsets.all(8),
                            child: Text(
                              'Select topics from the list',
                              textAlign: TextAlign.start,
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ),
                        dropdownItemDecoration: DropdownItemDecoration(
                          backgroundColor:
                              Theme.of(context).colorScheme.secondary,
                          selectedBackgroundColor:
                              Theme.of(context).colorScheme.secondary,
                          selectedIcon: const Icon(
                            Icons.check_box,
                            color: Colors.green,
                          ),
                          disabledIcon: Icon(
                            Icons.lock,
                            color: Colors.grey.shade300,
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please select a topic to continue';
                          }
                          return null;
                        },
                        onSelectionChange: (selectedItems) {
                          debugPrint("OnSelectionChange: $selectedItems");
                        },
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(
            height: 8,
          ),
          Expanded(
            child: ListView.builder(
              addAutomaticKeepAlives: true,
              controller: scrollController,
              itemCount: msgs.length,
              shrinkWrap: true,
              reverse: true,
              padding: const EdgeInsets.only(bottom: 70),
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: isTyping && index == 0
                      ? Column(
                          children: [
                            BubbleNormal(
                              text: msgs[0].msg,
                              isSender: true,
                              color: Theme.of(context).colorScheme.tertiary,
                              textStyle: TextStyle(
                                color: Theme.of(context).colorScheme.background,
                                fontWeight: FontWeight.w600,
                                fontSize: 16,
                              ),
                            ),
                            // TODO: Add Animation for 'Typing ...' pop-up
                            BubbleNormal(
                              text: 'Typing ...',
                              isSender: false,
                              color: Theme.of(context).colorScheme.secondary,
                              textStyle: TextStyle(
                                color: Theme.of(context).colorScheme.tertiary,
                              ),
                            ),
                          ],
                        )
                      : BubbleNormal(
                          text: msgs[index].msg,
                          isSender: msgs[index].isSender,
                          color: msgs[index].isSender
                              ? Theme.of(context).colorScheme.tertiary
                              : Theme.of(context).colorScheme.tertiary,
                          textStyle: TextStyle(
                            color: Theme.of(context).colorScheme.background,
                            fontWeight: FontWeight.w600,
                            fontSize: 16,
                          ),
                        ),
                );
              },
            ),
          ),
        ],
      ),
      primary: true,
      bottomSheet: Row(
        children: [
          // TODO: 'Add' Button functionality for adding Images, Documents, etc.
          IconButton(
            onPressed: () {},
            color: Theme.of(context).colorScheme.tertiary,
            iconSize: 40,
            icon: const Icon(
              Icons.add_circle,
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(
                right: 12.0,
                top: 12.0,
                bottom: 12.0,
                left: 5.0, // 5 - if ADD button and 12 - if NOT
              ),
              child: Container(
                width: double.infinity,
                height: 45,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: const EdgeInsets.only(left: 8.0),
                  child: TextField(
                    controller: controller,
                    textCapitalization: TextCapitalization.sentences,
                    onSubmitted: (value) {
                      sendMsg();
                    },
                    textInputAction: TextInputAction.send,
                    showCursor: true,
                    decoration: const InputDecoration(
                      border: InputBorder.none,
                      hintText: "Enter text",
                      hintStyle: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    style: const TextStyle(
                      fontFamily: 'MSReference2',
                    ),
                    cursorColor: Theme.of(context).colorScheme.tertiary,
                  ),
                ),
              ),
            ),
          ),
          InkWell(
            onTap: () {
              if (formKey.currentState?.validate() ?? false) {
                selectedItems = multiSelectController.selectedItems;
                sendMsg();
              }
            },
            child: Container(
              height: 40,
              width: 40,
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.tertiary,
                borderRadius: BorderRadius.circular(30),
              ),
              child: Icon(
                Icons.send,
                color: Theme.of(context).colorScheme.background,
              ),
            ),
          ),
          const SizedBox(
            width: 8,
          )
        ],
      ),
    );
  }

  Future<void> sendMsg() async {
    String text = controller.text;
    controller.clear();
    try {
      if (text.isNotEmpty) {
        setState(
          () {
            msgs.insert(
              0,
              Message(isSender: true, msg: text),
            );
            isTyping = true;
          },
        );
        scrollController.animateTo(0.0,
            duration: const Duration(seconds: 1), curve: Curves.easeOut);

        userQuery(text);
      }
    } on Exception {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            errorMessage.isNotEmpty
                ? errorMessage[0].msg
                : "Some error occurred, please try again!",
          ),
        ),
      );
    }
  }

  Future<void> userQuery(incomingQuery) async {
    try {
      var headers = {
        'X-API-KEY': dotenv.env['X_API_KEY']!,
        'Content-Type': 'application/json'
      };
      var request = http.Request(
        'POST',
        Uri.parse(
          dotenv.env['APP_DEPLOYMENT']!,
        ),
      );

      request.body = json.encode(
        {
          'incoming_query': incomingQuery,
          'topics': selectedItems.map((e) => e.value).toList(),
        },
      );
      request.headers.addAll(headers);

      http.StreamedResponse response = await request.send();
      var queryResponse = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        setState(
          () {
            isTyping = false;
            msgs.insert(
              0,
              Message(
                isSender: false,
                msg: jsonDecode(queryResponse)["answer"].toString().trimLeft(),
              ),
            );
            errorMessage.insert(
              0,
              Message(
                isSender: false,
                msg: jsonDecode(queryResponse)["error_message"]
                    .toString()
                    .trimLeft(),
              ),
            );
            scrollController.animateTo(0.0,
                duration: const Duration(seconds: 1), curve: Curves.easeOut);
          },
        );
      }
    } on Exception {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            errorMessage.isNotEmpty
                ? errorMessage[0].msg
                : "Some error occurred, please try again!",
          ),
        ),
      );
    }
  }
}
