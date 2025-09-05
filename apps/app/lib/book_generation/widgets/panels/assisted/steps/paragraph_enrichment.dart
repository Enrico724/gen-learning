import 'package:flutter/material.dart';

class EnrichmentStatusView extends StatelessWidget {
  final Map<String, String> enrichmentStatus;

  const EnrichmentStatusView({
    Key? key,
    required this.enrichmentStatus,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Book Enrichment Status',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: enrichmentStatus.length,
                itemBuilder: (context, index) {
                  final key = enrichmentStatus.keys.elementAt(index);
                  final value = enrichmentStatus[key];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text(key),
                      subtitle: Text(value ?? 'Unknown'),
                      leading: Icon(
                        value == 'Completed'
                            ? Icons.check_circle
                            : Icons.pending,
                        color: value == 'Completed' ? Colors.green : Colors.orange,
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
    );
  }
}