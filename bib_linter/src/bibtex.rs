use std::collections::HashMap;
use regex::Regex;

#[derive(Debug)]
pub struct BibEntry {
    pub entry_type: String,
    pub citation_key: String,
    pub fields: HashMap<String, String>,
}

pub fn parse_bibtex(entry: &str) -> Option<BibEntry> {
    let header_re = Regex::new(r"@(\w+)\s*\{\s*([^,]+),").ok()?;
    let field_re = Regex::new(r"(?m)^\s*(\w+)\s*=\s*\{(.*?)\},?\s*$").ok()?;

    let header_caps = header_re.captures(entry)?;
    let entry_type = header_caps.get(1)?.as_str().to_string();
    let citation_key = header_caps.get(2)?.as_str().to_string();

    let mut fields = HashMap::new();
    for cap in field_re.captures_iter(entry) {
        let key = cap.get(1)?.as_str().to_lowercase();
        let value = cap.get(2)?.as_str().to_string();
        fields.insert(key, value);
    }

    Some(BibEntry {
        entry_type,
        citation_key,
        fields,
    })
}
