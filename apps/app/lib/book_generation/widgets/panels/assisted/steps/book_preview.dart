import 'package:flutter/material.dart';

class BookPreview extends StatelessWidget {
  final List<Map<String, dynamic>> chapters;

  const BookPreview({super.key, required this.chapters});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: chapters.length,
      itemBuilder: (context, chapterIndex) {
        final chapter = chapters[chapterIndex];
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: ExpansionTile(
            title: Text(
              chapter['title'],
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            initiallyExpanded: true,
            children: [
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: chapter['subchapters'].length,
                itemBuilder: (context, subchapterIndex) {
                  final subchapter = chapter['subchapters'][subchapterIndex];
                  return Padding(
                    padding: const EdgeInsets.only(left: 16.0),
                    child: ExpansionTile(
                      title: Text(
                        subchapter['title'],
                        style: const TextStyle(
                            fontSize: 16, fontWeight: FontWeight.w600),
                      ),
                      initiallyExpanded: true,
                      children: [
                        ListView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: subchapter['paragraphs'].length,
                          itemBuilder: (context, paragraphIndex) {
                            final paragraph =
                                subchapter['paragraphs'][paragraphIndex];
                            return Padding(
                              padding: const EdgeInsets.only(left: 32.0),
                              child: Text(
                                paragraph,
                                style: const TextStyle(fontSize: 14),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  );
                },
              ),
            ],
          ),
        );
      },
    );
  }
}