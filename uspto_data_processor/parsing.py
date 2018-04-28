from xml.etree import ElementTree


def get_xml_root(xml_str):
    return ElementTree.fromstring(xml_str)


def parse_biblio(xml_root):
    #FIXME - Some documents do not have this field???
    xml_biblio = xml_root.find('us-bibliographic-data-grant')
    biblio = {}
    pub_doc = xml_biblio.find('./publication-reference/document-id')
    app_doc = xml_biblio.find('./application-reference/document-id')
    
    if app_doc:
        biblio['type'] = xml_biblio.find('application-reference').attrib.get('appl-type')
        biblio['ap_iso'] = app_doc.findtext('country')
        biblio['ap_no'] = app_doc.findtext('doc-number')
        biblio['ap_dt'] = app_doc.findtext('date')
    
    if pub_doc:
        biblio['pb_iso'] = pub_doc.findtext('country')
        biblio['pb_dt'] = pub_doc.findtext('date')
        biblio['pb_no'] = pub_doc.findtext('doc-number').lstrip('0')
        biblio['kind'] = pub_doc.findtext('kind')

    applicants = []
    for appl in xml_biblio.findall('./us-parties/us-applicants/us-applicant'):
        ap = {}
        ap['seq'] = int(appl.attrib.get('sequence'))
        ap['name'] = {
            'last': appl.findtext('./addressbook/last-name'),
            'first': appl.findtext('./addressbook/first-name'),
            'org': appl.findtext('./addressbook/orgname')
        }
        ap['addr'] = {
            'country': appl.findtext('./addressbook/address/country'),
            'state': appl.findtext('./addressbook/address/state'),
            'city': appl.findtext('./addressbook/address/city')
        }
        applicants.append(ap)
    biblio['applicants'] = applicants

    inventors = []
    for invent in xml_biblio.findall('./us-parties/inventors/inventor'):
        inv = {}
        inv['seq'] = int(invent.attrib.get('sequence'))
        inv['name'] = {
            'last': invent.findtext('./addressbook/last-name'),
            'first': invent.findtext('./addressbook/first-name')
        }
        # ap['type'] = appl.find('./addressbook/role').text
        inv['addr'] = {
            'country': invent.findtext('./addressbook/address/country'),
            'state': invent.findtext('./addressbook/address/state'),
            'city': invent.findtext('./addressbook/address/city')
        }
        inventors.append(inv)
    biblio['inventors'] = inventors

    agents = []
    for agent in xml_biblio.findall('./us-parties/agents/agent'):
        ag = {}
        ag['seq'] = int(agent.attrib.get('sequence'))
        ag['name'] = {
            'last': agent.findtext('./addressbook/last-name'),
            'first': agent.findtext('./addressbook/first-name'),
            'org': agent.findtext('./addressbook/orgname')
        }
        # ap['type'] = appl.find('./addressbook/role').text
        ag['addr'] = {
            'country': agent.findtext('./addressbook/address/country'),
            'state': agent.findtext('./addressbook/address/state'),
            'city': agent.findtext('./addressbook/address/city')
        }
        agents.append(ag)
    biblio['agents'] = agents

    assignees = []
    """
    for assignee type, one of the following codes is placed in the role element. Assignee types 
        for U.S. patents are taken from the following table: 
            01 Unassigned; 
            02 United States company or corporation;
            03 Foreign company or corporation;
            04 United States individual;
            05 Foreign individual;
            06 U.S. Federal government;
            07 Foreign government;
            08 U.S. county government;
            09 U.S. state government.
    """
    for idx, assgn in enumerate(xml_biblio.findall('./assignees/assignee'), start=1):
        an = {}
        an['seq'] = idx
        an['name'] = {
            'last': assgn.findtext('./addressbook/last-name'),
            'first': assgn.findtext('./addressbook/first-name'),
            'org': assgn.findtext('./addressbook/orgname')
        }
        an['type'] = assgn.findtext('./addressbook/role')
        an['addr'] = {
            'country': assgn.findtext('./addressbook/address/country'),
            'state': assgn.findtext('./addressbook/address/state'),
            'city': assgn.findtext('./addressbook/address/city')
        }
        assignees.append(an)
    biblio['assignees'] = assignees
        
    biblio['title'] = app_doc = xml_biblio.findtext('invention-title')
    
    return biblio


def parse_clms(xml_root):
    claims = {}
    for child in xml_root.find('claims').findall('claim'):
        claim = {}
        claim['id'] = child.attrib.get('id')
        claim['claim_no'] = int(child.attrib.get('num'))
        claim['text'] = child.findtext('claim-text').strip()

        claim['elements'] = []
        if child.find('claim-text').tail.strip():
            claim['elements'].append(child.find('claim-text').tail)

        ref = child.find('claim-text/claim-ref')
        claim['ref'] = ref.attrib['idref'] if ref is not None else None
        if child.find('claim-text').find('claim-ref') is not None:
            ref = child.find('claim-text').find('claim-ref')
            if ref.tail.strip(',\n '):
                claim['elements'].append(ref.tail.strip(', \n'))

        for el in child.findall('claim-text/claim-text'):
            claim['elements'].append(el.text.strip())

        claims[child.attrib.get('num').lstrip('0')] = claim

    return claims