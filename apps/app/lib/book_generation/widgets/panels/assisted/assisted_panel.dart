import 'package:app/book_generation/widgets/panels/assisted/steps/book_preview.dart';
import 'package:app/book_generation/widgets/panels/assisted/steps/book_structure.dart';
import 'package:app/book_generation/widgets/panels/assisted/steps/paragraph_enrichment.dart';
import 'package:flutter/material.dart';

class AssistedPanel extends StatefulWidget {
  const AssistedPanel({super.key});

  @override
  State<AssistedPanel> createState() => _AssistedPanelState();
}

class _AssistedPanelState extends State<AssistedPanel> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<Map<String, dynamic>> _sampleBookData = [
    {
      'title': 'Chapter 1: The Beginning',
      // The 'subchapters' key now matches what BookPreview expects.
      'subchapters': [
        {
          'title': 'Subchapter 1.1: First Steps',
          // The 'paragraphs' key now matches, and the value is a List<String>.
          'paragraphs': [
            'This is the first paragraph of the first subchapter.',
            'Here is another sentence to form the second paragraph.'
          ],
        },
        {
          'title': 'Subchapter 1.2: A New World',
          'paragraphs': [
            'The journey continued into a new world, full of wonders and dangers.'
          ],
        },
      ],
    },
    {
      'title': 'Chapter 2: The Journey',
      'subchapters': [
        {
          'title': 'Subchapter 2.1: The Road Ahead',
          'paragraphs': ['The road was long and winding.'],
        },
      ],
    },
  ];


  void _goToPage(int page) {
    _pageController.animateToPage(
      page,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
    setState(() {
      _currentPage = page;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 2,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Assisted Panel',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 16),
          Text(
            'This is the assisted panel where users can manually create and edit book structures.',
            style: TextStyle(fontSize: 16),
          ),
          Expanded(
            child: PageView(
              controller: _pageController,
              onPageChanged: (index) {
                setState(() {
                  _currentPage = index;
                });
              },
              children: [
                BookStructureEditor(),
                EnrichmentStatusView(
                  enrichmentStatus: {
                    'Paragraph 1': 'Completed',
                    'Paragraph 2': 'In Progress',
                    'Paragraph 3': 'Not Started',
                  },
                ),
                BookPreview(
                  chapters: _sampleBookData,
                ),
              ],
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              ElevatedButton(
                onPressed: _currentPage > 0
                    ? () => _goToPage(_currentPage - 1)
                    : null,
                child: Text('Previous'),
              ),
              ElevatedButton(
                onPressed: _currentPage < 2
                    ? () => _goToPage(_currentPage + 1)
                    : null,
                child: Text('Next'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
