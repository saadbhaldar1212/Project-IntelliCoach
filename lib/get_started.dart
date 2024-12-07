import 'package:fitness_advisor_chatbot/chat_screen.dart';
import 'package:fitness_advisor_chatbot/components/app_bar.dart';
import 'package:fitness_advisor_chatbot/components/elevated_button.dart';
import 'package:fitness_advisor_chatbot/components/text.dart';
import 'package:flutter/material.dart';

class GetStarted extends StatefulWidget {
  const GetStarted({super.key});

  @override
  State<GetStarted> createState() => _GetStartedState();
}

class _GetStartedState extends State<GetStarted> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: const MyAppBar(
        title: 'Fitness ChatBot v3.10',
      ),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const MyText(
                content: 'Fitness ChatBot v3.10',
                fontSize: 22,
                fontWeight: FontWeight.w600,
              ),
              MyElevatedButton(
                onPressed: () {
                  Navigator.pushAndRemoveUntil(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const ChatScreen(
                        chatScreenTitle: 'Fitness Chatbot v3.10',
                      ),
                    ),
                    (route) => false,
                  );
                },
                child: const MyText(
                  content: 'Get Started',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
