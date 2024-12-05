import 'package:fitness_advisor_chatbot/components/elevated_button.dart';
import 'package:fitness_advisor_chatbot/components/text.dart';
import 'package:flutter/material.dart';

import 'package:http/http.dart' show get, post;

class AboutMe extends StatelessWidget {
  const AboutMe({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: MyElevatedButton(
          child: const MyText(
            content: 'Click Me',
          ),
          onPressed: () => viewUsers(),
        ),
      ),
    );
  }

  Future<void> viewUsers(parsedJson) async {
    var headers = {
      'X-API-KEY':
          'f45b98763210cedfa45b98763210cedfa45b98763210cedfa45b98763210cedfa'
    };
    var request = http.Request(
      'POST',
      Uri.parse('http://localhost:8000/user'),
    );
    request.body = '''''';
    request.headers.addAll(headers);

    http.StreamedResponse response = await request.send();

    if (response.statusCode == 200) {
      print(await response.stream.bytesToString());
    } else {
      print(response.reasonPhrase);
    }
  }
}
