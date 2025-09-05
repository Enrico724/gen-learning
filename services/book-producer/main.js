/**
 * @fileoverview A Node.js Kafka consumer that generates a well-formatted PDF book
 * from a JSON message. It now includes Markdown support for bold, italics, and lists.
 * The Table of Contents is correctly placed at the beginning of the book.
 *
 * NOTE: This version requires the 'marked' library. Install it with: npm install marked
 */

// Importa le librerie necessarie
const { Kafka } = require('kafkajs');
const PDFDocument = require('pdfkit');
const fs = require('fs');
const { marked } = require('marked'); // Importa la libreria per il parsing del Markdown

// --- Configurazione di Kafka ---
const kafka = new Kafka({
    clientId: process.env.KAFKA_CLIENT_ID || 'kafka-book-consumer-app',
    brokers: (process.env.KAFKA_BOOTSTRAP_SERVERS || 'localhost:9092').split(',') // Legge i broker dall'env e li separa con la virgola
});

const TOPIC = 'generated-books';
const GROUP_ID = 'book-pdf-group-markdown-v6'; // Cambia il Group ID se vuoi riprocessare i messaggi
const consumer = kafka.consumer({ groupId: GROUP_ID });

/**
 * Renderizza una serie di token Markdown inline (grassetto, corsivo, testo normale).
 * @param {Array} tokens I token inline da renderizzare.
 * @param {PDFDocument} doc L'istanza del documento PDF.
 */
const renderInline = (tokens, doc) => {
    tokens.forEach(token => {
        const textOptions = { continued: true };
        switch (token.type) {
            case 'strong':
                doc.font('Helvetica-Bold').text(token.text, textOptions);
                break;
            case 'em':
                doc.font('Helvetica-Oblique').text(token.text, textOptions);
                break;
            case 'text':
            default:
                doc.font('Helvetica').text(token.text, textOptions);
                break;
        }
    });
};

/**
 * Analizza e renderizza una stringa di testo Markdown nel documento PDF.
 * @param {string} markdownText Il testo Markdown da renderizzare.
 * @param {PDFDocument} doc L'istanza del documento PDF.
 */
const renderMarkdown = (markdownText, doc) => {
    if (typeof markdownText !== 'string') return;

    const tokens = marked.lexer(markdownText);

    tokens.forEach(token => {
        switch (token.type) {
            case 'heading':
                const size = 20 - (token.depth * 2);
                doc.font('Helvetica-Bold').fontSize(size).text(token.text).moveDown(0.5);
                break;
            case 'paragraph':
                renderInline(token.tokens, doc);
                // **FIX**: Applica la giustificazione al paragrafo
                doc.text('', { align: 'justify' });
                doc.moveDown(0.5);
                break;
            case 'list':
                doc.font('Helvetica');
                token.items.forEach(item => {
                    const itemY = doc.y;
                    doc.text('• ', doc.page.margins.left, itemY, { continued: true });
                    renderInline(item.tokens[0].tokens, doc);
                    // **FIX**: Applica la giustificazione anche agli elementi degli elenchi
                    doc.text('', { align: 'justify' });
                });
                doc.moveDown(1);
                break;
            case 'space':
                doc.moveDown(1);
                break;
            default:
                if (token.raw) {
                    doc.font('Helvetica').fontSize(12).text(token.raw);
                }
                break;
        }
    });
};


/**
 * Funzione per creare un PDF elegante e strutturato da un oggetto libro.
 * @param {object} bookData L'oggetto JSON del libro.
 * @param {string} filename Il percorso e il nome del file di output.
 * @returns {Promise<void>} Una Promise che si risolve al completamento del PDF.
 */
const createPdf = (bookData, filename) => {
    return new Promise((resolve, reject) => {
        try {
            const doc = new PDFDocument({
                bufferPages: true,
                autoFirstPage: false,
                margin: 72,
                lineGap: 4 // Spazio verticale tra le righe per evitare sovrapposizioni
            });

            const stream = fs.createWriteStream(filename);
            doc.pipe(stream);

            const toc = [];
            let pageCounter = 0;

            // --- 1. Pagina del Titolo ---
            doc.addPage();
            pageCounter++;
            const title = typeof bookData.titolo_libro === 'string' ? bookData.titolo_libro : 'Titolo non disponibile';
            doc.font('Helvetica-Bold').fontSize(28)
               .text(title, { align: 'center' });


            // --- 2. Pagine per l'Indice (placeholder) ---
            doc.addPage();
            pageCounter++;
            const tocPage1Index = pageCounter - 1;

            doc.addPage();
            pageCounter++;
            const tocPage2Index = pageCounter - 1;


            // --- 3. Generazione del Contenuto ---
            doc.addPage();
            pageCounter++;

            (bookData.capitoli || []).forEach((chapter, chapterIndex) => {
                if (chapterIndex > 0) {
                    doc.addPage();
                    pageCounter++;
                }

                const chapterTitle = typeof chapter.titolo_capitolo === 'string' ? chapter.titolo_capitolo : `Capitolo ${chapterIndex + 1}`;
                toc.push({
                    title: chapterTitle,
                    page: pageCounter,
                    level: 1,
                    destination: `chapter-${chapterIndex}`
                });
                
                doc.addNamedDestination(`chapter-${chapterIndex}`);
                doc.font('Helvetica-Bold').fontSize(18).text(chapterTitle);
                doc.moveDown(1);

                (chapter.sottocapitoli || []).forEach((subchapter, subchapterIndex) => {
                    if (doc.y > doc.page.height - doc.page.margins.bottom - 100) {
                        doc.addPage();
                        pageCounter++;
                    }
                
                    const subchapterTitle = typeof subchapter.titolo_sottocapitolo === 'string' ? subchapter.titolo_sottocapitolo : 'Sottocapitolo senza titolo';
                    toc.push({
                        title: subchapterTitle,
                        page: pageCounter,
                        level: 2,
                        destination: `subchapter-${chapterIndex}-${subchapterIndex}`
                    });

                    doc.addNamedDestination(`subchapter-${chapterIndex}-${subchapterIndex}`);
                    doc.font('Helvetica-Bold').fontSize(14).text(subchapterTitle);
                    doc.moveDown(0.5);

                    (subchapter.paragrafi || []).forEach(paragraphText => {
                        renderMarkdown(paragraphText, doc);
                    });
                    doc.moveDown(1);
                });
            });

            // --- 4. Riempimento dell'Indice ---
            let currentPageIndex = tocPage1Index;
            doc.switchToPage(currentPageIndex);
            doc.y = doc.page.margins.top;

            doc.font('Helvetica-Bold').fontSize(20).text('Indice', { align: 'center' });
            doc.moveDown(1.5);

            const pageBottom = doc.page.height - doc.page.margins.bottom;

            toc.forEach(item => {
                if (doc.y > pageBottom - 20) {
                    currentPageIndex = tocPage2Index;
                    doc.switchToPage(currentPageIndex);
                    doc.y = doc.page.margins.top;
                    // Ripete il titolo "Indice" in modo professionale, senza "(continua)"
                    doc.font('Helvetica-Bold').fontSize(20).text('Indice', { align: 'center' });
                    doc.moveDown(1.5);
                }

                const x = item.level === 1 ? doc.page.margins.left : doc.page.margins.left + 18;
                const font = item.level === 1 ? 'Helvetica-Bold' : 'Helvetica';
                const size = item.level === 1 ? 12 : 11;
                
                const y = doc.y;
                doc.font(font).fontSize(size).text(item.title, x, y, {
                    link: item.destination,
                    goTo: item.destination,
                });
    
                doc.font('Helvetica').fontSize(size).text(item.page.toString(), doc.page.margins.left, y, {
                    align: 'right'
                });
                // Aumenta la spaziatura verticale tra le righe dell'indice
                doc.y = y + doc.currentLineHeight() + 8;
            });
            
            const lastTocPage = doc.switchToPage(tocPage2Index);
            if (lastTocPage.content.length === 0) {
                 doc.deletePage(tocPage2Index);
                 pageCounter--;
            }


            // --- 5. Aggiunta dei Numeri di Pagina (Footer) ---
            const totalPages = pageCounter;
            for (let i = 0; i < totalPages; i++) {
                if (i === 0) continue;
                
                doc.switchToPage(i);
                const pageNumber = i + 1;
                const footerY = doc.page.height - doc.page.margins.bottom + 10;
                doc.fontSize(9).font('Helvetica')
                   .text(`Pagina ${pageNumber} di ${totalPages}`, 
                   doc.page.margins.left, 
                   footerY, 
                   { 
                       align: 'center', 
                       width: doc.page.width - doc.page.margins.left - doc.page.margins.right 
                   });
            }

            doc.end();
            stream.on('finish', resolve);
            stream.on('error', reject);
        } catch (error) {
            reject(error);
        }
    });
};

// --- Logica di esecuzione del consumer ---
const run = async () => {
    try {
        await consumer.connect();
        await consumer.subscribe({ topic: TOPIC, fromBeginning: true });

        console.log(`In attesa di messaggi dal topic "${TOPIC}" per il gruppo "${GROUP_ID}"...`);

        await consumer.run({
            eachMessage: async ({ message }) => {
                try {
                    const bookData = JSON.parse(message.value.toString());

                    if (typeof bookData !== 'object' || bookData === null) {
                        console.error(`Messaggio ignorato: i dati del libro non sono un oggetto valido. Dati ricevuti: ${message.value.toString()}`);
                        return;
                    }

                    const safeTitle = (typeof bookData.titolo_libro === 'string' ? bookData.titolo_libro : 'libro_senza_titolo').replace(/[\s\W]+/g, '_');
                    const filename = `./pdfs/${safeTitle}.pdf`;

                    if (!fs.existsSync('./pdfs')) {
                        fs.mkdirSync('./pdfs', { recursive: true });
                    }

                    console.log(`Messaggio ricevuto. Creazione del PDF per: ${bookData.titolo_libro}`);
                    await createPdf(bookData, filename);
                    console.log(`PDF "${filename}" creato con successo!`);
                } catch (error)
                 {
                    console.error(`Errore durante l'elaborazione del messaggio: ${error.message}`);
                    console.error(error.stack);
                }
            },
        });
    } catch (error) {
        console.error('Errore nella connessione o esecuzione del consumer:', error);
    }
};

run();
