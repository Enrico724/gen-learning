import 'package:app/book_generation/widgets/create_gen_book_button.dart';
import 'package:app/book_generation/widgets/history_book_list_tile.dart';
import 'package:app/book_generation/widgets/panels/assisted/assisted_panel.dart';
import 'package:app/book_generation/widgets/panels/automated/automated_panel.dart';
import 'package:flutter/material.dart';

class BookGenerationScreen extends StatelessWidget {
  final bool isAutomated;
  final String title;
  final String description;

  const BookGenerationScreen({
    super.key,
    required this.isAutomated,
    this.title = "Book Generation",
    this.description = "Generate your books easily.",
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Book Generation')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // --- Colonna di sinistra: Side menu ---
              Container(
                width: 200, // Fixed width for the side menu
                color: Colors.grey[200], // Background color for the side menu
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CreateGenBookButton(onPressed: () {}),
                    const SizedBox(height: 20),
                    const Divider(color: Colors.black, thickness: 2),
                    const Text(
                      'Storico',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 10),
                    // Lista di rettangoli per lo storico
                    ...List.generate(5, (i) => Column(
                      children: [
                        HistoryBookListTile(
                          title: 'Book Title $i',
                          onTap: () {},
                        ),
                        const SizedBox(height: 10),
                      ],
                    )),
                    const SizedBox(height: 10),
                  ],
                ),
              ),

              const SizedBox(width: 30), // Spazio tra le due colonne
              // --- Colonna di destra: Main content ---
              isAutomated ? const AutomatedPanel() : const AssistedPanel(),

            ],
          ),
        ),
      ),
    );
  }
}
