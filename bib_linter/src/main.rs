use std::fs;
use std::path::Path;
use regex::Regex;

fn main() {
    let path = "data/sources.bib";
    if !Path::new(path).exists() {
        eprintln!("File '{}' not found.", path);
        return;
    }

    let content = fs::read_to_string(path)
        .expect("Failed to read the .bib file");

    // Basic regex to match bib entries
    let entry_re = Regex::new(r"(?s)@.*?\{.*?\n(.*?\n)*?}").unwrap();

    let entries: Vec<String> = entry_re
        .find_iter(&content)
        .map(|m| m.as_str().trim().to_string())
        .collect();

    println!("Found {} entries.", entries.len());

    // Optional: print the first one
    if let Some(first) = entries.first() {
        println!("First entry:\n{}\n", first);
    }
}
