import 'package:flutter/material.dart';

class ParamsWidget extends StatelessWidget {
  const ParamsWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Parametri',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const Text(
              'CTX',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),
        // Linee di punti per i parametri e CTX
        _buildParameterDots(),
        const SizedBox(height: 5),
        _buildParameterDots(),
        const SizedBox(height: 5),
        _buildParameterDots(),
        const SizedBox(height: 20),
      ],
    );
  }

  Widget _buildParameterDots() {
    return Row(
      children: List.generate(10, (index) {
        return const Padding(
          padding: EdgeInsets.symmetric(horizontal: 2),
          child: Icon(
            Icons.circle,
            size: 8,
            color: Colors.grey,
          ),
        );
      }),
    );
  }
}