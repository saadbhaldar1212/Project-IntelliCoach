import 'package:fitness_advisor_chatbot/chat_screen.dart';
import 'package:fitness_advisor_chatbot/get_started.dart';
import 'package:fitness_advisor_chatbot/theme/theme.dart';
import 'package:fitness_advisor_chatbot/theme/theme_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => ThemeProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fitness Chatbot v3.10',
      home: const GetStarted(),
      // const ChatScreen(chatScreenTitle: 'Fitness Chatbot v3.10'),
      debugShowCheckedModeBanner: false,
      theme: Provider.of<ThemeProvider>(context).themeData,
    );
  }
}
