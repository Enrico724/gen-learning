import 'package:flutter/material.dart';

class ScenarioCard extends StatelessWidget {
  final String title;
  final String description;
  final String featureLabel;

  const ScenarioCard({
    super.key,
    required this.title,
    required this.description,
    required this.featureLabel,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final maxWidth = constraints.maxWidth * 0.3; // Max size as 30% of screen width
        final width = maxWidth.clamp(80.0, 420.0); // Clamp width between 80 and 420
        return Card(
          elevation: 4,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          child: Container(
            height: 160, // Adjusted height for better spacing
            width: width,
            padding: const EdgeInsets.all(16.0), // Increased padding
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      Icons.tips_and_updates, // Idea icon
                      size: 28,
                      color: Colors.blueAccent,
                    ),
                    const SizedBox(
                      width: 12,
                    ), // Increased spacing between icon and text
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.start,
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
                const SizedBox(
                  height: 12,
                ), // Spacing between content and chip
                Align(
                  alignment: Alignment.centerLeft,
                  child: Chip(
                    label: Text(
                      featureLabel, // Feature label passed as argument
                      style: const TextStyle(
                        fontSize: 12,
                        color: Colors.white,
                      ),
                    ),
                    backgroundColor: Colors.blueAccent, // Chip background color
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}