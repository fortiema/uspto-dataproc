from xml.etree import ElementTree


def parse_biblio(xml_biblio):
    biblio = {}
    pub_doc = xml_biblio.find('publication-reference').find('document-id')
    app_doc = xml_biblio.find('application-reference').find('document-id')
    
    if app_doc:
        biblio['type'] = xml_biblio.find('application-reference').attrib.get('appl-type')
        biblio['ap_iso'] = app_doc.find('country').text
        biblio['ap_no'] = app_doc.find('doc-number').text
        biblio['ap_dt'] = app_doc.find('date').text
    
    if pub_doc:
        biblio['pb_iso'] = pub_doc.find('country').text
        biblio['pb_dt'] = pub_doc.find('date').text
        biblio['pb_no'] = pub_doc.find('doc-number').text
        biblio['kind'] = pub_doc.find('kind').text
        
    biblio['title'] = app_doc = xml_biblio.find('invention-title').text
    
    return biblio


def parse_clms(xml_clms):
    claims = {}
    for child in xml_clms.findall('claim'):
        _id = child.attrib.get('id')
        claims[_id] = {}
        claims[_id]['id'] = _id
        claims[_id]['text'] = child.find('claim-text').text.strip()

        claims[_id]['elements'] = []
        if child.find('claim-text').tail.strip():
            claims[_id]['elements'].append(child.find('claim-text').tail)

        ref = child.find('claim-text').find('claim-ref')
        claims[_id]['ref'] = ref.attrib['idref'] if ref is not None else None
        if child.find('claim-text').find('claim-ref') is not None:
            ref = child.find('claim-text').find('claim-ref')
            if ref.tail.strip(',\n '):
                claims[_id]['elements'].append(ref.tail.strip(', \n'))

        for el in child.find('claim-text').findall('claim-text'):
            claims[_id]['elements'].append(el.text.strip())

    return claims