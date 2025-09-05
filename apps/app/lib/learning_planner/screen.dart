import 'package:app/learning_planner/widgets/plan_generator_input.dart';
import 'package:app/learning_planner/widgets/timeline.dart';
import 'package:flutter/material.dart';

class LearningPlannerScreen extends StatelessWidget {
  const LearningPlannerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Learning Planner')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // --- Left Column: Side menu ---
              Container(
              width: 200, // Fixed width for the side menu
              color: Colors.grey[200], // Background color for the side menu
              child: ListView(
                padding: const EdgeInsets.all(8.0),
                children: [
                const Divider(color: Colors.black, thickness: 2),
                const Text(
                  'History',
                  style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 10),
                // List of history items
                ...List.generate(5, (i) => ListTile(
                    title: Text('Plan Title $i'),
                    onTap: () {},
                  )),
                ],
              ),
              ),

              Expanded(
                child: Column(
                  children: const [
                    PlanGeneratorInput(),
                    Timeline()
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}