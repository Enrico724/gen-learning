import 'package:flutter/material.dart';

class Timeline extends StatelessWidget {
  const Timeline({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemCount: 10, // Number of points
        itemBuilder: (context, index) {
          return Card(
        margin: const EdgeInsets.symmetric(vertical: 8.0),
        child: ListTile(
          leading: Icon(Icons.calendar_today, color: Colors.green),
          title: Text('Day ${index + 1} - Day ${index + 2}'),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
          Text('Title for Point ${index + 1}', style: TextStyle(fontWeight: FontWeight.bold)),
          SizedBox(height: 4.0),
          Text(
            'This is a detailed description for Point ${index + 1}. It provides more information about the day or range of days.',
            style: TextStyle(color: Colors.grey[600]),
          ),
            ],
          ),
          onTap: () {
            // Handle tile tap
          },
        ),
          );
        },
      ),
    );
  }
}
