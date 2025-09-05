import 'package:flutter/material.dart';

class QuickGenInput extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final void Function(String)? onSubmitted;

  const QuickGenInput({
    super.key,
    required this.controller,
    this.hintText = '',
    this.onSubmitted,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey), // Outline the component
        borderRadius: BorderRadius.circular(8), // Rounded corners
      ),
      padding: EdgeInsets.all(8), // Add some padding inside the outline
      child: SizedBox(
        width: 300, // Set a fixed width
        height: 50, // Set a fixed height
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: controller,
                decoration: InputDecoration(
                  hintText: hintText,
                  border: InputBorder.none, // Remove the border
                ),
                onSubmitted: onSubmitted,
              ),
            ),
            SizedBox(width: 8), // Add spacing between the text field and button
            Material(
              color: Colors.blue, // Set the background color
              borderRadius: BorderRadius.circular(
                8,
              ), // Rounded corners for the button
              child: InkWell(
                onTap: () {
                  if (onSubmitted != null) {
                    onSubmitted!(
                      controller.text,
                    ); // Trigger onSubmitted with text
                  }
                },
                borderRadius: BorderRadius.circular(
                  8,
                ), // Match the button's border radius
                child: Container(
                  padding: EdgeInsets.all(8), // Add padding inside the button
                  child: Icon(
                    Icons.send,
                    color: Colors.white,
                    size: 24,
                  ), // Adjust the icon size
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
