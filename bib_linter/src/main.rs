mod bibtex;
mod utils;

use std::fs;
use std::path::Path;
use regex::Regex;
use bibtex::parse_bibtex;
use utils::field_matches_any_ci;

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

    for entry in &entries {
        if let Some(entry) = parse_bibtex(entry) {
            // todo make this list more extensive
            let arxiv_names = ["arxiv", "biorxiv", "somethingelse..."];
            if field_matches_any_ci(&entry, "journal", &arxiv_names) {
                // todo check out this scraper...
                // https://github.com/bertof/gscite/blob/main/src/lib.rs
                // https://medium.com/@darshankhandelwal12/web-scraping-google-with-rust-6c80fa55234f

                println!("This entry is from a known journal.");
                println!("{}", entry.citation_key);
                println!("{}", entry.entry_type);
                for (key, value) in entry.fields.iter() {
                    println!("{}: {}", key, value);
                }
            }
            // } else {
            //     println!("Journal not recognized.");
            // }
            // println!("Citation Key: {}", entry.citation_key);
            // println!("Entry Type: {}", entry.entry_type);
            // for (key, value) in entry.fields.iter() {
            //     println!("{}: {}", key, value);
            // }
        } else {
            println!("Failed to parse BibTeX entry.");
        }
    }
}
