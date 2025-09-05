import 'package:flutter/material.dart';

class PlanGeneratorInput extends StatelessWidget {
  const PlanGeneratorInput({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 50,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black, width: 2),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Row(
        children: [
          Container(
            width: 50,
            decoration: BoxDecoration(
              border: Border(
                right: BorderSide(color: Colors.black, width: 2),
              ),
            ),
            child: const Center(
              child: Text('L', style: TextStyle(fontSize: 20)),
            ),
          ),
          const Spacer(),
          const Padding(
            padding: EdgeInsets.only(right: 8.0),
            child: Icon(Icons.play_arrow, size: 30),
          ),
        ],
      ),
    );
  }
}