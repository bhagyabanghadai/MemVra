package com.compyle.memvra.util;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class PdfExtractor {
    public static void main(String[] args) throws IOException {
        if (args.length == 0) {
            System.err.println("Usage: PdfExtractor <absolute-pdf-path>");
            System.exit(2);
        }
        String pdfPath = args[0];
        File pdf = new File(pdfPath);
        if (!pdf.exists()) {
            System.err.println("PDF not found: " + pdf.getAbsolutePath());
            System.exit(3);
        }

        try (PDDocument doc = PDDocument.load(pdf)) {
            int pages = doc.getNumberOfPages();
            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(doc);

            Path outDir = Path.of("build", "pdf");
            Files.createDirectories(outDir);
            Path outFile = outDir.resolve("extracted.txt");
            Files.writeString(outFile, text, StandardCharsets.UTF_8);

            System.out.println("[PdfExtractor] Extracted text to: " + outFile.toAbsolutePath());
            System.out.println("[PdfExtractor] Pages: " + pages + ", Characters: " + text.length());

            // Print a short excerpt to console for quick inspection
            int excerptLen = Math.min(2000, text.length());
            String excerpt = text.substring(0, excerptLen).replaceAll("\r", "");
            System.out.println("\n--- BEGIN EXCERPT ---\n");
            System.out.println(excerpt);
            System.out.println("\n--- END EXCERPT ---\n");
        }
    }
}