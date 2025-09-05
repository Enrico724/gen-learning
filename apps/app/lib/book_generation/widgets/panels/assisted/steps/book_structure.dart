import 'package:flutter/material.dart';

class BookStructureEditor extends StatefulWidget {
  const BookStructureEditor({super.key});

  @override
  State<BookStructureEditor> createState() => _BookStructureEditorState();
}

class _BookStructureEditorState extends State<BookStructureEditor> {
  List<Map<String, dynamic>> chapters = [
    {
      'title': 'Chapter 1',
      'subchapters': [
        {
          'title': 'Subchapter 1.1',
          'paragraphs': ['Paragraph 1.1.1', 'Paragraph 1.1.2'],
        },
        {
          'title': 'Subchapter 1.2',
          'paragraphs': ['Paragraph 1.2.1'],
        },
      ],
    },
    {
      'title': 'Chapter 2',
      'subchapters': [
        {
          'title': 'Subchapter 2.1',
          'paragraphs': ['Paragraph 2.1.1'],
        },
      ],
    },
  ];

  void addChapter() {
    setState(() {
      chapters.add({
        'title': 'Chapter ${chapters.length + 1}',
        'subchapters': [],
      });
    });
  }

  void addSubchapter(int chapterIndex) {
    setState(() {
      chapters[chapterIndex]['subchapters'].add({
        'title':
            'Subchapter ${chapters[chapterIndex]['subchapters'].length + 1}',
        'paragraphs': [],
      });
    });
  }

  void addParagraph(int chapterIndex, int subchapterIndex) {
    setState(() {
      chapters[chapterIndex]['subchapters'][subchapterIndex]['paragraphs'].add(
        'Paragraph ${chapters[chapterIndex]['subchapters'][subchapterIndex]['paragraphs'].length + 1}',
      );
    });
  }

  void deleteChapter(int chapterIndex) {
    setState(() {
      chapters.removeAt(chapterIndex);
    });
  }

  void deleteSubchapter(int chapterIndex, int subchapterIndex) {
    setState(() {
      chapters[chapterIndex]['subchapters'].removeAt(subchapterIndex);
    });
  }

  void deleteParagraph(int chapterIndex, int subchapterIndex, int paragraphIndex) {
    setState(() {
      chapters[chapterIndex]['subchapters'][subchapterIndex]['paragraphs']
          .removeAt(paragraphIndex);
    });
  }

  void updateTitle(int chapterIndex, String newTitle) {
    setState(() {
      chapters[chapterIndex]['title'] = newTitle;
    });
  }

  void updateSubchapterTitle(
      int chapterIndex, int subchapterIndex, String newTitle) {
    setState(() {
      chapters[chapterIndex]['subchapters'][subchapterIndex]['title'] =
          newTitle;
    });
  }

  void updateParagraph(
      int chapterIndex, int subchapterIndex, int paragraphIndex, String newText) {
    setState(() {
      chapters[chapterIndex]['subchapters'][subchapterIndex]['paragraphs']
          [paragraphIndex] = newText;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: chapters.length,
      itemBuilder: (context, chapterIndex) {
        final chapter = chapters[chapterIndex];
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: ExpansionTile(
            leading: IconButton(
              icon: Icon(Icons.delete, color: Colors.red),
              onPressed: () => deleteChapter(chapterIndex),
            ),
            title: TextField(
              controller: TextEditingController(text: chapter['title']),
              onSubmitted: (value) => updateTitle(chapterIndex, value),
              decoration: InputDecoration(border: InputBorder.none),
              minLines: 1,
              maxLines: null,
            ),
            initiallyExpanded: true,
            children: [
              ListView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                itemCount: chapter['subchapters'].length,
                itemBuilder: (context, subchapterIndex) {
                  final subchapter = chapter['subchapters'][subchapterIndex];
                  return Padding(
                    padding: const EdgeInsets.only(left: 16.0),
                    child: ExpansionTile(
                      leading: IconButton(
                        icon: Icon(Icons.delete, color: Colors.red),
                        onPressed: () =>
                            deleteSubchapter(chapterIndex, subchapterIndex),
                      ),
                      title: TextField(
                        controller: TextEditingController(text: subchapter['title']),
                        onSubmitted: (value) =>
                            updateSubchapterTitle(chapterIndex, subchapterIndex, value),
                        decoration: InputDecoration(border: InputBorder.none),
                        minLines: 1,
                        maxLines: null,
                      ),
                      initiallyExpanded: true,
                      children: [
                        ListView.builder(
                          shrinkWrap: true,
                          physics: NeverScrollableScrollPhysics(),
                          itemCount: subchapter['paragraphs'].length,
                          itemBuilder: (context, paragraphIndex) {
                            final paragraph =
                                subchapter['paragraphs'][paragraphIndex];
                            return Padding(
                              padding: const EdgeInsets.only(left: 32.0),
                              child: ListTile(
                                leading: IconButton(
                                  icon: Icon(Icons.delete, color: Colors.red),
                                  onPressed: () => deleteParagraph(
                                      chapterIndex, subchapterIndex, paragraphIndex),
                                ),
                                title: TextField(
                                  controller: TextEditingController(text: paragraph),
                                  onSubmitted: (value) => updateParagraph(
                                      chapterIndex, subchapterIndex, paragraphIndex, value),
                                  decoration: InputDecoration(border: InputBorder.none),
                                  minLines: 1,
                                  maxLines: null,
                                ),
                              ),
                            );
                          },
                        ),
                        Padding(
                          padding: const EdgeInsets.only(left: 32.0),
                          child: TextButton(
                            onPressed: () =>
                                addParagraph(chapterIndex, subchapterIndex),
                            child: Text('Add Paragraph'),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
              Padding(
                padding: const EdgeInsets.only(left: 16.0),
                child: TextButton(
                  onPressed: () => addSubchapter(chapterIndex),
                  child: Text('Add Subchapter'),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
