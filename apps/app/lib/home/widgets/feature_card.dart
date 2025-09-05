import 'package:flutter/material.dart';

class FeatureCard extends StatelessWidget {
  final String title;
  final String description;
  final VoidCallback onTap; // Callback to handle navigation

  const FeatureCard({
    super.key,
    required this.title,
    required this.description,
    required this.onTap, // Required onTap parameter
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final maxWidth = constraints.maxWidth * 0.3; // Max size as 30% of screen width
        final width = maxWidth.clamp(80.0, 420.0); // Clamp width between 80 and 420
        return GestureDetector(
          onTap: onTap, // Trigger navigation when tapped
          child: Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            child: Container(
              height: 140, // Increased height for better spacing
              width: width,
              padding: const EdgeInsets.all(16.0), // Increased padding
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start, // Align icon and title to the top
                children: [
                  Icon(
                    Icons.lightbulb,
                    size: 28,
                    color: Colors.amber,
                  ), // Icon representing a feature
                  const SizedBox(
                    width: 12,
                  ), // Increased spacing between icon and text
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.start, // Align content to the top
                      children: [
                        Text(
                          title, // Title passed as argument
                          style: const TextStyle(
                            fontSize: 18, // Increased font size for better readability
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(
                          height: 8,
                        ), // Increased spacing between title and description
                        Text(
                          description, // Description passed as argument
                          style: const TextStyle(
                            fontSize: 14, // Slightly larger font size for description
                            color: Colors.black87, // Softer black for better readability
                            height: 1.5, // Increased line height for better readability
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}