import 'dart:async';
import 'package:fitness_advisor_chatbot/components/app_bar.dart';

import 'message.dart';
import 'package:chat_bubbles/bubbles/bubble_normal.dart';
import 'package:flutter/material.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key, required this.chatScreenTitle});

  final String chatScreenTitle;

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  TextEditingController controller = TextEditingController();
  ScrollController scrollController = ScrollController();
  List<Message> msgs = [];
  bool isTyping = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MyAppBar(
        title: widget.chatScreenTitle,
      ),
      body: Column(
        children: [
          const SizedBox(
            height: 8,
          ),
          Expanded(
            child: ListView.builder(
              controller: scrollController,
              itemCount: msgs.length,
              shrinkWrap: true,
              reverse: true,
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
                            )
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
                          ),
                        ),
                );
              },
            ),
          ),
          Row(
            children: [
              // TODO: 'Add' Button for adding Images, Documents, etc.
              // IconButton(
              //   onPressed: () {},
              //   color: Theme.of(context).colorScheme.tertiary,
              //   iconSize: 40,
              //   icon: const Icon(
              //     Icons.add_circle_sharp,
              //   ),
              // ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(
                    right: 12.0,
                    top: 12.0,
                    bottom: 12.0,
                    left: 12.0, // 5 - if ADD button
                  ),
                  child: Container(
                    width: double.infinity,
                    height: 45,
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.only(
                        left: 12,
                        right: 12,
                        bottom: 2,
                      ),
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
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              InkWell(
                onTap: () {
                  sendMsg();
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
        ],
      ),
    );
  }

  void sendMsg() async {
    String text = controller.text;
    controller.clear();
    // String apiKey =
    //     "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";
    // try {
    //   if (text.isNotEmpty) {
    //     setState(
    //       () {
    //         msgs.insert(
    //           0,
    //           Message(true, text),
    //         );
    //         isTyping = true;
    //       },
    //     );
    //     scrollController.animateTo(0.0,
    //         duration: const Duration(seconds: 1), curve: Curves.easeOut);
    //     var response = await http.post(
    //       Uri.parse("https://api.openai.com/v1/chat/completions"),
    //       headers: {
    //         "Authorization": "Bearer $apiKey",
    //         "Content-Type": "application/json"
    //       },
    //       body: jsonEncode(
    //         {
    //           "model": "gpt-4o-mini",
    //           "messages": [
    //             {"role": "user", "content": text}
    //           ]
    //         },
    //       ),
    //     );
    //     if (response.statusCode == 200) {
    //       var json = jsonDecode(response.body);
    //       setState(
    //         () {
    //           isTyping = false;
    //           msgs.insert(
    //             0,
    //             Message(
    //               false,
    //               json["choices"][0]["message"]["content"]
    //                   .toString()
    //                   .trimLeft(),
    //             ),
    //           );
    //         },
    //       );
    //       scrollController.animateTo(0.0,
    //           duration: const Duration(seconds: 1), curve: Curves.easeOut);
    //     }
    //   }
    // } on Exception {
    //   ScaffoldMessenger.of(context).showSnackBar(
    //     const SnackBar(
    //       content: Text("Some error occurred, please try again!"),
    //     ),
    //   );
    // }
    try {
      if (text.isNotEmpty) {
        setState(
          () {
            msgs.insert(
              0,
              Message(true, text),
            );
            isTyping = true;
          },
        );
        scrollController.animateTo(0.0,
            duration: const Duration(seconds: 1), curve: Curves.easeOut);

        Timer(
          const Duration(seconds: 3),
          () {
            setState(
              () {
                isTyping = false;
                msgs.insert(
                  0,
                  Message(
                    false,
                    'Hello! How can I assist you?',
                  ),
                );
              },
            );
            scrollController.animateTo(0.0,
                duration: const Duration(seconds: 1), curve: Curves.easeOut);
          },
        );
      }
    } on Exception {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Some error occurred, please try again!"),
        ),
      );
    }
  }
}
