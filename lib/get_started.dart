import 'package:fitness_advisor_chatbot/chat_screen.dart';
import 'package:fitness_advisor_chatbot/components/app_bar.dart';
import 'package:fitness_advisor_chatbot/components/elevated_button.dart';
import 'package:fitness_advisor_chatbot/components/text.dart';
import 'package:fitness_advisor_chatbot/theme/theme.dart';
import 'package:flutter/material.dart';

class GetStarted extends StatefulWidget {
  const GetStarted({super.key});

  @override
  State<GetStarted> createState() => _GetStartedState();
}

class _GetStartedState extends State<GetStarted> {
  double _customOpacity = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: const MyAppBar(
        title: '',
      ),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              TweenAnimationBuilder(
                onEnd: () {
                  setState(() {
                    _customOpacity = 1;
                  });
                },
                curve: Curves.easeInOutCirc,
                tween: Tween<double>(begin: 0, end: 200),
                duration: const Duration(seconds: 1),
                builder: (context, value, child) => Hero(
                  tag: 'getStartedScreenLogo',
                  child: Image.asset(
                    Theme.of(context).colorScheme == darkMode.colorScheme
                        ? 'assets/images/darkModeLogoPNG.png'
                        : 'assets/images/lightModeLogoPNG.png',
                    height: value,
                    width: value,
                  ),
                ),
              ),
              Column(
                children: [
                  AnimatedOpacity(
                    opacity: _customOpacity,
                    duration: const Duration(milliseconds: 500),
                    child: const MyText(
                      content: 'IntelliCoach',
                      fontSize: 30,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  AnimatedOpacity(
                    opacity: _customOpacity,
                    duration: const Duration(milliseconds: 500),
                    child: const MyText(
                      content: 'Fitness ChatBot',
                      fontSize: 14,
                      fontWeight: FontWeight.w400,
                    ),
                  ),
                  const SizedBox(height: 20),
                  AnimatedOpacity(
                    opacity: _customOpacity,
                    duration: const Duration(milliseconds: 500),
                    child: MyElevatedButton(
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
                  ),
                ],
              ),
              const SizedBox(
                height: 50,
              )
            ],
          ),
        ],
      ),
    );
  }
}
