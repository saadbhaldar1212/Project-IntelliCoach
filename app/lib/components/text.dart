import 'package:flutter/material.dart';

class MyText extends StatelessWidget {
  const MyText(
      {super.key,
      required this.content,
      this.fontSize,
      this.fontWeight,
      this.color});

  final String content;
  final double? fontSize;
  final FontWeight? fontWeight;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    return Text(
      content,
      style: TextStyle(
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color,
      ),
    );
  }
}
