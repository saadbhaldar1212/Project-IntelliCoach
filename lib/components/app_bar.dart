import 'package:fitness_advisor_chatbot/components/text.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../theme/theme.dart';
import '../theme/theme_provider.dart';

class MyAppBar extends StatefulWidget implements PreferredSizeWidget {
  const MyAppBar({
    super.key,
    this.title,
    this.centerTitle = false,
  });

  final String? title;
  final bool? centerTitle;

  @override
  State<MyAppBar> createState() => _MyAppBarState();

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

class _MyAppBarState extends State<MyAppBar> {
  @override
  Widget build(BuildContext context) {
    return AppBar(
      elevation: 0,
      actions: [
        IconButton(
          onPressed: () {
            Provider.of<ThemeProvider>(context, listen: false).toggleTheme();
          },
          icon: Provider.of<ThemeProvider>(context).themeData == lightMode
              ? const Icon(
                  Icons.sunny,
                )
              : const Icon(
                  Icons.dark_mode,
                ),
        ),
      ],
      backgroundColor: Theme.of(context).colorScheme.background,
      title: MyText(
        content: widget.title!,
      ),
      centerTitle: widget.centerTitle,
    );
  }
}
