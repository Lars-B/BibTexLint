use crate::bibtex::BibEntry;

pub fn field_matches_any_ci(entry: &BibEntry, key: &str, targets: &[&str]) -> bool {
    if let Some(value) = entry.fields.get(key) {
        let value_lc = value.to_lowercase();
        targets.iter().any(|&target| value_lc == target.to_lowercase())
    } else {
        false
    }
}
