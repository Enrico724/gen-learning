import 'package:flutter/material.dart';

import 'widgets/automated_input.dart';
import 'widgets/params.dart';

class AutomatedPanel extends StatelessWidget {
  const AutomatedPanel({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 2,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Automated Panel',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 16),
          ParamsWidget(),
          AutomatedInputWidget(),
        ],
      ),
    );
  }
}
