import 'package:fitness_advisor_chatbot/chat_screen.dart';
import 'package:fitness_advisor_chatbot/core/database/connect.dart';
import 'package:fitness_advisor_chatbot/get_started.dart';
import 'package:fitness_advisor_chatbot/theme/theme_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  await dotenv.load(fileName: 'lib/.flutter_env');
  WidgetsFlutterBinding.ensureInitialized();
  // await MongoDatabase.connect();
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
      title: 'IntelliCoach - Fitness Chatbot v3.10',
      home: const GetStarted(),
      // const ChatScreen(chatScreenTitle: 'Fitness Chatbot v3.10')
      debugShowCheckedModeBanner: false,
      theme: Provider.of<ThemeProvider>(context).themeData,
      themeAnimationDuration: const Duration(milliseconds: 35),
    );
  }
}
