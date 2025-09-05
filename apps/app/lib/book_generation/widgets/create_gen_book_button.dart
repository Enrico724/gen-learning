import 'package:flutter/material.dart';

class CreateGenBookButton extends StatelessWidget {
  final VoidCallback onPressed;

  const CreateGenBookButton({super.key, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: const Text(
      'New',
      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      ),
      label: const Icon(Icons.add, size: 28),
      style: ElevatedButton.styleFrom(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      elevation: 0, // No elevation
      ),
    );
  }
}