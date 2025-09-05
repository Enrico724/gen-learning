import 'package:app/home/widgets/book_history_icon_button.dart';
import 'package:app/home/widgets/feature_card.dart';
import 'package:app/home/widgets/quick_gen_input.dart';
import 'package:app/home/widgets/scenario_card.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedChip = 0;
  final TextEditingController _quickGenController = TextEditingController();

  @override
  void dispose() {
    _quickGenController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // --- Sezione "Home" e filtri in alto ---
              const Text(
                'Home',
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  QuickGenInput(
                    controller: _quickGenController,
                    hintText: "Quick Generate text",
                  ),
                  const SizedBox(width: 10),
                  BookHistoryIconButton(onPressed: () {}),
                ],
              ),
              const SizedBox(height: 20),

              // --- Prima riga di rettangoli ---
              Center(
                child: Wrap(
                  spacing: 20.0, // Horizontal spacing between items
                  runSpacing: 20.0, // Vertical spacing between rows
                  alignment: WrapAlignment.center, // Center align the items
                    children: [
                    FeatureCard(
                      title: 'Automated Book Generation',
                      description: 'Generate books automatically with predefined settings to save time and ensure consistency in your content creation process.',
                      onTap: () {
                      Navigator.pushNamed(
                        context, 
                        '/book_generation', 
                        arguments: {'isAutomated': true},
                      );
                      },
                    ),
                    FeatureCard(
                      title: 'Manual Book Generation',
                      description: 'Create books manually by customizing every detail to suit your specific needs and preferences.',
                      onTap: () {
                      Navigator.pushNamed(
                        context,
                        '/book_generation',
                        arguments: {'isAutomated': false},
                      );
                      },
                    ),
                    FeatureCard(
                      title: 'Learning Planner',
                      description: 'Plan your learning journey with customizable schedules and progress tracking.',
                      onTap: () {
                      Navigator.pushNamed(
                        context,
                        '/learning_planner',
                      );
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // --- Seconda riga di quadrati inclinati ---
              const SizedBox(height: 20),
              const Align(
                alignment: Alignment.bottomLeft,
                child: Text(
                  'Scenarios',
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.w500),
                ),
              ),
              const SizedBox(height: 20),
              Wrap(
                spacing: 20.0, // Horizontal spacing between items
                runSpacing: 20.0, // Vertical spacing between rows
                children: List.generate(6, (index) {
                  return ScenarioCard(
                    title: 'Scenario ${index + 1}',
                    description: 'Description for Scenario ${index + 1}',
                    featureLabel: 'Feature ${index + 1}',
                  );
                }),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
