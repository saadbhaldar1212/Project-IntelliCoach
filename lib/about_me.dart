import 'package:fitness_advisor_chatbot/components/text.dart';
import 'package:flutter/material.dart';

class AboutMe extends StatefulWidget {
  const AboutMe({super.key});

  @override
  State<AboutMe> createState() => _AboutMeState();
}

class _AboutMeState extends State<AboutMe> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: MyText(
          content: "No output",
        ),
      ),
    );
  }
}
