import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json

# https://info.arxiv.org/help/api/user-manual.html

def query_arxiv(keywords, start=0, max_results=10):
    """
    Query the arXiv API with the given parameters and return results in JSON format.
    
    Args:
        keywords (list): List of keyword phrases to search for
        start (int): Starting index of results
        max_results (int): Maximum number of results to return
    
    Returns:
        dict: JSON formatted results
    """
    # Build the search query with proper encoding
    search_parts = []
    for keyword in keywords:
        # Encode the keyword properly - quotes become %22, spaces become %20
        encoded_keyword = urllib.parse.quote(f'"{keyword}"', safe='')
        search_parts.append(f"all:{encoded_keyword}")
    
    # Join search parts with + sign
    search_query = "+".join(search_parts)
    
    # Construct the API URL with relevance sorting
    url = f'http://export.arxiv.org/api/query?search_query={search_query}&sortBy=relevance&start={start}&max_results={max_results}'
    
    print(url)
    
    # Make the request
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    
    # Parse the XML response
    root = ET.fromstring(data)
    
    # Define namespace mapping
    namespaces = {
        '': 'http://www.w3.org/2005/Atom',
        'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    # Extract general information
    result = {
        'total_results': int(root.find('.//opensearch:totalResults', namespaces).text),
        'start_index': int(root.find('.//opensearch:startIndex', namespaces).text),
        'items_per_page': int(root.find('.//opensearch:itemsPerPage', namespaces).text),
        'entries': []
    }
    
    # Extract each entry
    for entry in root.findall('.//entry', namespaces):
        entry_data = {
            'id': entry.find('./id', namespaces).text,
            'title': entry.find('./title', namespaces).text.strip(),
            'summary': entry.find('./summary', namespaces).text.strip(),
            'published': entry.find('./published', namespaces).text,
            'updated': entry.find('./updated', namespaces).text,
            'authors': [],
            'links': [],
        }
        
        # Extract authors
        for author in entry.findall('./author', namespaces):
            author_data = {
                'name': author.find('./name', namespaces).text
            }
            
            affiliation = author.find('./arxiv:affiliation', namespaces)
            if affiliation is not None:
                author_data['affiliation'] = affiliation.text
                
            entry_data['authors'].append(author_data)
        
        # Extract links
        for link in entry.findall('./link', namespaces):
            link_data = {
                'href': link.attrib.get('href'),
                'rel': link.attrib.get('rel'),
                'type': link.attrib.get('type')
            }
            
            if 'title' in link.attrib:
                link_data['title'] = link.attrib.get('title')
                
            entry_data['links'].append(link_data)
        
        # Extract additional arXiv-specific fields if present
        doi = entry.find('./arxiv:doi', namespaces)
        if doi is not None:
            entry_data['doi'] = doi.text
            
        comment = entry.find('./arxiv:comment', namespaces)
        if comment is not None:
            entry_data['comment'] = comment.text
            
        journal_ref = entry.find('./arxiv:journal_ref', namespaces)
        if journal_ref is not None:
            entry_data['journal_ref'] = journal_ref.text
            
        primary_category = entry.find('./arxiv:primary_category', namespaces)
        if primary_category is not None:
            entry_data['primary_category'] = primary_category.attrib.get('term')
            
        # Get all categories
        categories = []
        for category in entry.findall('./category', namespaces):
            categories.append(category.attrib.get('term'))
        
        if categories:
            entry_data['categories'] = categories
            
        result['entries'].append(entry_data)
    
    return result

# Example usage
if __name__ == "__main__":
    # # Single keyword phrase
    # results = query_arxiv(["quantum computing"])
    # print(json.dumps(results, ensure_ascii=False, indent=4))
    
    # # Multiple keyword phrases
    # results = query_arxiv(["semantic networks", "large language model", "natural language processing"])
    # print(json.dumps(results, ensure_ascii=False, indent=4))
    
    # With pagination parameters
    results = query_arxiv(["machine learning", "neural networks"], start=10, max_results=5)
    print(json.dumps(results, ensure_ascii=False, indent=4))