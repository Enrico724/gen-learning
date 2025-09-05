import 'package:app/book_generation/screen.dart';
import 'package:app/home/screen.dart';
import 'package:app/learning_planner/screen.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DidacticGen',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => HomeScreen(),
        '/learning_planner': (context) => LearningPlannerScreen(),
        '/book_generation': (context) {
          final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
          final isAutomated = args?['isAutomated'] ?? false;
          return BookGenerationScreen(isAutomated: isAutomated);
        },
      },
    );
  }
}
