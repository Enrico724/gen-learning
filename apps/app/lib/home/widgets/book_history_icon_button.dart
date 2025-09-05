import 'package:flutter/material.dart';

class BookHistoryIconButton extends StatelessWidget {
  final VoidCallback onPressed;

  const BookHistoryIconButton({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: IconButton(
        icon: Icon(Icons.history),
        tooltip: 'Book History',
        onPressed: onPressed,
      ),
    );
  }
}