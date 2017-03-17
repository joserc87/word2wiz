use strict;
use warnings;
use List::MoreUtils;
use Archive::Zip;
use File::Slurp;
use List::MoreUtils qw(uniq);
use File::Basename;

# sub-routine om strings te trimmen
sub  trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };

# Loop through all the .docx files in a directory
my @files = <$ARGV[0]/*.docx>;
my $file = "";
my $numFiles = @files;
print "Aantal docx documenten: " . $numFiles . "\n";

foreach $file (@files) {
	print $file . "\n";
	my $baseFile = basename($file, ".docx");
	my $xmlFile = $ARGV[0] . "/" . $baseFile . ".xml";
	my $txtFile = $ARGV[0] . "/" . $baseFile . ".txt";
	print $xmlFile . "\n";

#unzip Word file
my $zipname = $file;
my $destinationDirectory = './unpack';
my $zip = Archive::Zip->new($zipname);
my @matches;

foreach my $member ($zip->members) {
    next if $member->isDirectory;
    (my $extractName = $member->fileName) =~ s{.*/}{};
    $member->extractToFileNamed("$destinationDirectory/$extractName");
}

print "Word file extracted to ./unpack/\n";
print "Stripping the XML tags...\n";

# open file for stripping
my $word_document = read_file('./unpack/document.xml');

$word_document =~ s|<.+?>||g;

open FILE3, ">", "./unpack/document.txt" or die $!;
print FILE3 $word_document;
close FILE3;

# open file in utf-8
open FILE, "<:encoding(UTF-8)", "./unpack/document.txt" or die $!;

# parse file (find field names) and push in array
while (<FILE>) {
#		push @matches, (lc($_) =~ m/«(.*?)»/g);
		push @matches, ($_) =~ m/«(.*?)»/g;
}

foreach(@matches) {
	$_ =~ s/^\s+|\s+$//g;
	# whitespace verwijderen
	$_ =~ s/\s+/ /g;
}

my $counter = 0;
my @checkboxes;
my @defaultvalues;

#foreach(@matches) {
#	if ($matches[$counter] eq 'naam land') {
#			$matches[$counter] = 'verwijderen';
#			last;
#	}
#	$counter++;
#}

# Pull all default values from the document and remove entries from array
my $defaultonderwerptekst =				"";
my $defaultondertekenaar  = 			"";
my $defaultfunctieondertekenaar = "";
my $defaultbijlageuploaden = 			"";
my $defaultmedischecategorie = 			"Medisch Declaratie";

$counter = 0;
my $defaultvaluesCounter = 0;
foreach(@matches) {
	# print $_ . "\n";
	if ($matches[$counter] =~ /default/) {
		# print $_ . "\n";
		$defaultvalues[$defaultvaluesCounter] = substr($matches[$counter], 0);
		# defaultonderwerptekst
		if (length $defaultvalues[$defaultvaluesCounter] > 22) {
			if ($defaultvalues[$defaultvaluesCounter] =~ 'defaultonderwerptekst') {
				$defaultonderwerptekst = substr($defaultvalues[$defaultvaluesCounter], 22);
			}
		}
		# defaultondertekenaar
		if (length $defaultvalues[$defaultvaluesCounter] > 21) {
			if ($defaultvalues[$defaultvaluesCounter] =~ 'defaultondertekenaar') {
				$defaultondertekenaar = substr($defaultvalues[$defaultvaluesCounter], 21);
			}
		}
		# defaultfunctieondertekenaar
		if (length $defaultvalues[$defaultvaluesCounter] > 28) {
			if ($defaultvalues[$defaultvaluesCounter] =~ 'defaultfunctieondertekenaar') {
				$defaultfunctieondertekenaar = substr($defaultvalues[$defaultvaluesCounter], 28);
				$defaultfunctieondertekenaar = ucfirst $defaultfunctieondertekenaar;
			}
		}
		
		if (length $defaultvalues[$defaultvaluesCounter] > 25) {
			if ($defaultvalues[$defaultvaluesCounter] =~ 'defaultmedischecategorie') {
				$defaultmedischecategorie = substr($defaultvalues[$defaultvaluesCounter], 25);
				$defaultmedischecategorie = ucfirst $defaultmedischecategorie;
			}
		}
		# defaultbijlageuploaden
		if (length $defaultvalues[$defaultvaluesCounter] > 23) {
			if ($defaultvalues[$defaultvaluesCounter] =~ 'defaultbijlageuploaden') {
				$defaultbijlageuploaden = substr($defaultvalues[$defaultvaluesCounter], 23);
				$defaultbijlageuploaden = uc $defaultbijlageuploaden;
				if ($defaultbijlageuploaden eq "JA") {
					$defaultbijlageuploaden = "True";
				} else {
					$defaultbijlageuploaden = "False";
				}
			}
		}
		$matches[$counter] = 'verwijderen';
		$defaultvaluesCounter++;
	}
	$counter++;
}

print "DEFAULTONDERWERPTEKST = " . $defaultonderwerptekst . "\n";
print "DEFAULTONDERTEKENAAR = " . $defaultondertekenaar . "\n";
print "DEFAULTFUNCTIEONDERTEKENAAR = " . $defaultfunctieondertekenaar . "\n";
print "DEFAULTBIJLAGEUPLOADEN = " . $defaultbijlageuploaden . "\n";
print "DEFAULTMEDISCHECATEGORIE = " . $defaultmedischecategorie . "\n";

# Pull all checkboxes from user fields and remove entries from array
#$counter = 0;
#my $checkboxCounter = 0;
#foreach(@matches) {
	# print $_ . "\n";
#	if ($matches[$counter] =~ /checkbox/) {
#		print "CHECKBOX: " . $matches[$counter] . "\n"; 
#		$checkboxes[$checkboxCounter] = substr($matches[$counter], 9);
#		$checkboxes[$checkboxCounter] =~ s/^\s+//;
#		$checkboxes[$checkboxCounter++] =~ s/\s+$//;		
		#$matches[$counter] = 'checkbox ' . $matches[$counter];
#	}
#	$counter++;
#}

# remove unwanted matches
@matches = grep {$_ ne 'verwijderen' } @matches;
@matches = grep {$_ ne 'altijd' } @matches;
@matches = grep {$_ ne 'leeg invulveld (onderwerp brief)' } @matches;
@matches = grep {$_ ne 'geslacht' } @matches;
@matches = grep {$_ ne 'voorletters'} @matches;
@matches = grep {$_ ne 'naam'} @matches;
@matches = grep {$_ ne 'straat'} @matches;
@matches = grep {$_ ne 'huisnummer'} @matches;
@matches = grep {$_ ne 'postcode'} @matches;
@matches = grep {$_ ne 'woonplaats'} @matches;
@matches = grep {$_ ne 'land'} @matches;
@matches = grep {$_ ne 'aanhef_naam'} @matches;
@matches = grep {$_ ne 'doc-id invoeren'} @matches;
@matches = grep {$_ ne 'd oc-id invoeren'} @matches;
@matches = grep {$_ ne 'doc - id invoeren'} @matches;
@matches = grep {$_ ne 'doc- id invoeren'} @matches;
@matches = grep {$_ ne 'creatie_datum'} @matches;
@matches = grep {$_ ne 'maak de volgende keuze. behandeling toets 1, consult toets 2, onderzoek toets 3,'} @matches;
@matches = grep {$_ ne 'verznr/relnr'} @matches;
@matches = grep {$_ ne 'mw_afdelingstelefoon'} @matches;
@matches = grep {$_ ne 'mw_afdelingsfax'} @matches;
@matches = grep {$_ ne 'mw_naam'} @matches;
@matches = grep {$_ ne 'mw_initialen'} @matches;
@matches = grep {$_ ne 'mw_afdeling'} @matches;
@matches = grep {$_ ne 'org_internet'} @matches;
@matches = grep {$_ ne 'org_dsadresverzekerden'} @matches;
@matches = grep {$_ ne 'org_dspostcodeverzekerden'} @matches;
@matches = grep {$_ ne 'org_dsplaatsverzekerden'} @matches;
@matches = grep {$_ ne 'org_emailadresklachten'} @matches;
@matches = grep {$_ ne 'org_adres'} @matches;
@matches = grep {$_ ne 'org_postcode'} @matches;
@matches = grep {$_ ne 'org_woonplaats'} @matches;
@matches = grep {$_ ne 'org_internet'} @matches;
@matches = grep {$_ ne 'org_banknrpremie'} @matches;
@matches = grep {$_ ne 'org_naamrekeninghouder'} @matches;
@matches = grep {$_ ne 'org_av_algemeen'} @matches;
@matches = grep {$_ ne 'org_dsadreszorgverleners'} @matches;
@matches = grep {$_ ne 'org_dspostcodezorgverleners'} @matches;
@matches = grep {$_ ne 'org_dsplaatszorgverleners'} @matches;
@matches = grep {$_ ne 'lb_uzovicode'} @matches;
@matches = grep {$_ ne 'lb_internet'} @matches;
@matches = grep {$_ ne 'lb_tekst'} @matches;
@matches = grep {$_ ne 'LB_tekst'} @matches;
@matches = grep {$_ ne 'lb _tekst'} @matches;
@matches = grep {$_ ne 'lb_naam'} @matches;

# Dubbele verwijderen
my @unique_matches = uniq @matches;

open FILE2, ">:encoding(UTF-8)", "$xmlFile" or die $!;
open FILE4, ">:encoding(UTF-8)", "$txtFile" or die $!;

# Set the values from Composition Center
# Waarden uit CC toekennen
my @metadataName = (
"txt_001",
"txt_002",
"txt_003",
"txt_004",
"txt_005",
"txt_006",
"txt_007",
"txt_008",
"txt_009",
"txt_010",
"txt_011",
"txt_012",
"txt_013",
"txt_014",
"txt_015",
"txt_016",
"txt_017",
"txt_018",
"txt_019",
"txt_020",
"txt_021",
"txt_022",
"txt_023",
"txt_024",
"txt_025",
"txt_026",
"txt_027",
"txt_028",
"txt_029",
"txt_030",
"txt_031",
"txt_032",
"txt_033",
"txt_034",
"txt_035",
"txt_036",
"txt_037",
"txt_038",
"txt_039",
"txt_040",
"txt_041",
"txt_042",
"txt_043",
"txt_044",
"txt_045",
"txt_046",
"txt_047",
"txt_048",
"txt_049",
"txt_050");

# GUID's van omgeving Achmea
# =====================================
my @metadataGUID = (
"b7be1136-33ca-4d44-9010-c2d44a8f8c7d",
"c2d12f08-d647-4b13-8ee1-c70d0ef425b6",
"a40f7698-fe4d-452d-a48b-56ee39d24fa5",
"79962f29-dc44-4824-948d-a28f49ba8ab9",
"394b0b55-dcab-48ea-b620-263528306afd",
"39576235-f636-4a38-b13e-85001f0a7262",
"15328532-9d12-4069-afea-b0388805a05a",
"cbcf9067-4c81-4ca3-b708-ab332ebdef85",
"c1ff1561-2b2b-4270-b138-e9602660afea",
"325364e9-b098-41a9-a4d5-8a59f8721ed6",
"60995c29-d940-43d8-ac0a-ad1e036f1592",
"3e4fc2ab-9183-4a53-85a5-a866cfa68e01",
"e8258af1-5824-44ad-9450-a2b4bcb22779",
"3524b9d2-d6ce-4c06-b767-505d04c1716f",
"5175e3c4-7a59-4ab4-931d-5152e894cf0b",
"742e5b38-550e-4918-84d5-c760142912bb",
"7b1a9c27-90a9-4df6-b908-889b8c8dab97",
"a9f090fa-ba99-44f0-bb9d-0fb386f3c6a0",
"8126a292-a4e2-41c2-8ebb-4e8f765efdf5",
"7f6de42f-bd8d-45e0-9a2e-1bf546cfb755",
"70e7a003-b29b-482d-87c0-aab5802f5371",
"2905e9b8-9ece-4fa5-8027-81c286ca8cc3",
"edaa38a2-65b2-4fed-94d5-5051d218f4e9",
"bee5daca-dbc9-4b39-b30e-15c25882a337",
"b09ebaec-f73e-4bc3-b132-5f4a536924b3",
"c360c12b-2ff6-4d7e-9443-8f5972997827",
"bed9ce16-0933-4ca1-b990-a1738cfcdd64",
"05c6e6cd-db63-4c93-a7a7-ea8529da259c",
"56d3c689-970e-4ad1-bc7c-f3448dfe4ba5",
"90be48d2-a3a3-4d79-8b04-914bdcc061bc",
"184f4c0d-c042-4f79-867b-708c29caadcb",
"8b502497-d2b3-4f57-8948-e2b6bd0f0518",
"b65c7db2-306a-48c6-9d45-debf53d351d3",
"e3f23105-6251-419c-9b13-17bc137693c5",
"9689f45f-6422-4c69-8d4a-ac7f5dab7272",
"34172a6d-4e95-4807-9175-d5996ac7dac9",
"a83beec0-19d0-409d-a3d2-80f63980ed71",
"59b3dd66-5d9e-4630-a454-c7876b90ae6a",
"97f9f703-c068-4c88-9dcf-8a640741c416",
"889701ff-e8ec-41f3-9c5a-75f53b22a009",
"128534cb-22cb-4706-8630-ae251d2c2b72",
"d574c426-29a5-470f-b372-bb1906bca5f8",
"1d1efe54-942a-4c17-8f49-9d2baa5e65c8",
"107da73e-005b-4325-b4d0-27c5da65cfd7",
"d2bf5007-74b9-43a3-8ee9-6704240cf3ea",
"566e5ed8-7a58-44a6-930b-1654792ee941",
"43e54092-a4cd-4676-bd35-f992d7f88073",
"dd13f4e9-0403-46cd-be0e-cb2533a268a2",
"8b6ed40e-112d-4c82-a1db-bd8c6873c154",
"c2cea9ed-99ee-4c70-83a9-e8fbf67ed622");
# =====================================

# GUID's van omgeving TCF
# ======================================
# my @metadataGUID = (
# "cc9030a8-bec5-4182-8ea7-4b990b1da492",
# "2ad2964a-69bc-490d-b62b-9c5704666b0e",
# "6e9200bc-d8fd-4952-95a8-c5f9316843e8",
# "50c1674d-345e-4cf7-b9ff-c57463f5bec9",
# "1f89d732-3677-4c27-a73c-70584db5af4d",
# "5252d692-cc8c-4666-8ad3-a0677b9e281f",
# "11dd0fac-cf03-431b-bb64-cc11c2a5b78c",
# "ff994f56-994f-4f36-9f70-98056f031d37",
# "d242345a-43c2-49ba-bd90-eae2ac56a7e4",
# "6c17bb1f-fe8e-4582-bd70-94192d889cce",
# "a9f2d591-7b3b-4a1b-96c7-79739aeeb15f",
# "91f51c0d-8597-4c7b-84b5-fc6225190bae",
# "f83050b5-a2d1-4acd-af1a-5a9e039ba893",
# "be8fe661-d960-4948-8f18-2a0c1b8fb2b3",
# "16e86160-0837-4aed-9efd-b1806b5ed944",
# "09ff1e51-310e-46d5-87da-a89b7e412f78",
# "bb38c567-d9ca-4c79-a1de-9a9c7421d0bf",
# "3b65dc30-a534-4540-a3c5-5ae5bfa1210f",
# "f565f6c3-b166-46d7-9e99-1be1cdd35132",
# "7b8be602-946d-4197-a6d6-26a8c4605111",
# "9fab5b04-28d6-4f3a-b6bd-1f0fecaca2b0",
# "474bba58-9d14-4bc3-99b3-43bfaeaedb08",
# "fff43991-a2a0-4306-b344-d2809a746aa3",
# "0011d820-ab26-4d39-b5f8-c4924290fa34",
# "0529f267-2d15-44a0-b02c-13deafc0a918",
# "4ebd4af3-e8c8-438e-85da-eafaa3c21adb",
# "a0973b99-45e3-4684-8c95-77440debfd68",
# "cc63f91e-7af6-4846-81e7-9b7f16777733",
# "e102fa43-0136-4e24-9d34-f341fb822f85",
# "f53cd75b-0e49-4038-82c2-7273cb7227f3",
# "4ed99d13-44fd-4750-ba14-bf2574f9a587",
# "0e6cf5b3-dea9-4e51-8d58-33b5cc849d38",
# "3ee56f21-ee58-47cc-92d1-50f203934dbc",
# "bd5bee2c-d182-4c50-812f-c9763b1ddf55",
# "b42c7a1c-4fe3-4721-8edb-30a0c36ee34d",
# "db2b9985-eb87-45df-acf0-7731fea7f388",
# "13f26741-9fde-4ad1-8a4c-a4d0e71488f7",
# "d449f6a0-7016-4dd2-8d79-0a3c654cc680",
# "27a70ae6-c051-47bc-b88f-7b6c1a007e3a",
# "b3283994-7f01-46a5-a088-87c50240d9db",
# "60476c14-1e5b-431e-b33c-18c297979f36",
# "bddb1856-b071-46d7-ab8d-9f05d2f3b95e",
# "59ac5ea8-0008-42b9-b474-1c21a94f229a",
# "301a0ba7-c044-480b-b03a-13676a86f18a",
# "5d20eb65-c5ca-4ec5-a81e-e22a6c8d427f",
# "6e1297f1-b8aa-40a5-b1e4-3662f9da03a1",
# "ba6b2d28-52a4-4c67-9172-65b49300bc56",
# "82e8ecd1-beb4-43b5-bca4-06735712ff8b",
# "33bc458c-82cf-4cde-9889-56942732d3cf",
# "d9b0a812-d5c2-467f-ab0d-17e1d89a085e");

# Render the Wizard XML
# First the header
print FILE2 "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
print FILE2 "<!-- created with TCF parseWord -->\n";
print FILE2 "<Wizard xmlns=\"http://www.thedocumentwizard.nl/wizardconfiguration/2.0\" documentTypeName=\"vrzFMC\" name=\"" . $baseFile . "\">\n";
print FILE2 "<Steps>\n";
print FILE2 "<Step id=\"1\" name=\"Algemeen\" groupName=\"Buitenland\" type=\"START\" nextStepID=\"2\">\n";
print FILE2 "<AdvancedRules>\n";
print FILE2 "<AdvancedRule>\n";
print FILE2 "<Equal>\n";
print FILE2 "<Const val=\"hello world\" />\n";
print FILE2 "<Const val=\"hello world\" />\n";
print FILE2 "</Equal>\n";
print FILE2 "<Metadatas>\n";

# Now populate the metadata with the values from the Word file
# my $currentArray = 0;
my $metadataArray = 0;

#foreach (@checkboxes) {
#	print FILE2 "<Metadata id=\"" . $metadataGUID[$metadataArray++] . "\" name=\"" . $checkboxes[$currentArray] . "\">«" . $checkboxes[$currentArray++] . "»</Metadata>\n";
#}

#$currentArray = 0;

#foreach (@unique_matches) {
#	print FILE2 "<Metadata id=\"" . $metadataGUID[$metadataArray++] . "\" name=\"" . $unique_matches[$currentArray] . "\">«" . $unique_matches[$currentArray++] . "»</Metadata>\n";
#}

# Continue with the XML template
print FILE2 "</Metadatas>\n";
print FILE2 "</AdvancedRule>\n";
print FILE2 "</AdvancedRules>\n";
print FILE2 "<Questions>\n";
print FILE2 "<Question id=\"RU_001\" name=\"Referentienummer:\">\n";
print FILE2 "<!--RU_001-->\n";
print FILE2 "<String id=\"RU_001_1\" metadataID=\"a96dfa3d-0b24-4612-a17c-0825b4dba224\" metadataName=\"org_RefNr\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"RU_002\" name=\"Onderwerp:\" required=\"true\">\n";
print FILE2 "<!--RU_002-->\n";

# Defaultwaarde onderwerp van de brief invullen
print FILE2 "<String id=\"RU_002_1\" metadataID=\"ede12414-d7ef-4969-9d55-dd08c005fb4f\" metadataName=\"briefonderwerp\" defaultValue=\"" . $defaultonderwerptekst . "\"/>\n";
# =============================================

print FILE2 "</Question>\n";
print FILE2 "<Question name=\"\" id=\"RU_003A\">\n";
print FILE2 "<Label defaultValue=\"Ondertekenaar\" id=\"RU_003A_1\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question name=\"\" required=\"true\" id=\"RU_003\">\n";
print FILE2 "<!--RU_003-->\n";

# Defaultwaarde radiobutton 'medisch adviseur' of 'naam' bepalen
print FILE2 "<Radio id=\"RU_003_1\" defaultValue=\"" . $defaultondertekenaar . "\">\n";
# ==============================================================

print FILE2 "<Items>\n";

# Radiobutton ondertekenaar 'medisch adviseur'
print FILE2 "<Multi id=\"margot smits\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<Label defaultValue=\"Margot Smits - Senior medisch adviseur\" id=\"label_margot\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1a\" defaultValue=\"Margot Smits\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\" hidden=\"true\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1aa\" defaultValue=\"Senior medisch adviseur\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" hidden=\"true\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "<Multi id=\"wendy haanschoten\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<Label defaultValue=\"Wendy Haanschoten - Adviserend apotheker\" id=\"label_wendy\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1b\" defaultValue=\"Wendy Haanschoten\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\" hidden=\"true\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1bb\" defaultValue=\"Adviserend apotheker\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" hidden=\"true\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "<Multi id=\"marjolein rijkeboer\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<Label defaultValue=\"Marjolein Rijkeboer - Adviserend psycholoog\" id=\"label_marjolein\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1c\" defaultValue=\"Marjolein Rijkeboer\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\" hidden=\"true\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1cc\" defaultValue=\"Adviserend psycholoog\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" hidden=\"true\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "<Multi id=\"herman flens\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<Label defaultValue=\"Herman Flens - Medisch adviseur\" id=\"label_herman\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1d\" defaultValue=\"Herman Flens\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\" hidden=\"true\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1dd\" defaultValue=\"Medisch adviseur\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" hidden=\"true\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "<Multi id=\"job van huizen\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<Label defaultValue=\"Job van Huizen - Medisch adviseur\" id=\"label_job\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1e\" defaultValue=\"Job van Huizen\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\" hidden=\"true\"/>\n";
print FILE2 "<Label id=\"RU_003_1_1_1ee\" defaultValue=\"Medisch adviseur\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" hidden=\"true\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
# ============================================

# Radiobutton ondertekenaar 'naam'
print FILE2 "<Multi id=\"medewerker\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"RU_003_1_2_2\" defaultValueMetadataID = \"6ff7f4e2-0bfb-4b05-8fee-0b6cdbce7f6f\" metadataID=\"0430e988-80e5-4a4e-8146-467b4b47d157\" metadataName=\"ondertekenaar_naam\"/>\n";

# Defaultwaarde functie ondertekenaar van de brief invullen
print FILE2 "<List id=\"List_003_1\" metadataID=\"c4d06d64-f574-4300-a38a-0231f560c1a5\" metadataName=\"ondertekenaar_functie\" defaultValue=\"" . $defaultfunctieondertekenaar . "\">\n";
# =========================================================

print FILE2 "<Items>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medewerker declaratieservice</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Klachtcoördinator</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Klachtbehandelaar</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Specialist machtigingen</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "</Items>\n";
print FILE2 "</List>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
# ================================

print FILE2 "</Items>\n";
print FILE2 "</Radio>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"List\" name=\"Indien gewenst, verander optioneel de Medische Categorie van deze brief.\" required=\"true\">\n";
print FILE2 "<List id=\"List_1\" metadataID=\"1b603922-dd32-457e-99cf-b6bf13669717\" metadataName=\"medischecategorie_default\" defaultValue=\"" . $defaultmedischecategorie . "\">\n";
print FILE2 "<Items>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Polis</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Machtiging</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Declaratie</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Declaratie Dossier</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Zorgbemiddel</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Verhaal</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch AWBZ</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Medisch Arbo</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Polis</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Standaard</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Marketing</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "<Item>\n";
print FILE2 "<Value>Financieel</Value>\n";
print FILE2 "</Item>\n";
print FILE2 "</Items>\n";
print FILE2 "</List>\n";
print FILE2 "</Question>\n";
print FILE2 "</Questions>\n";
print FILE2 "</Step>\n";

# **************
# *** STAP 2 ***
# **************
#print FILE2 "<Step id=\"2\" name=\"Selecteer de optionele tekstblokken die van toepassing zijn.&#60;br&#62;Document: &#60;b&#62;" . $baseFile . "&#60;/b&#62;\" groupName=\"BUITENLAND\" type=\"STEP\" nextStepID=\"3\">\n";
#print FILE2 "<Questions>\n";

# Now the detailed questions
#$currentArray = 0;
#$metadataArray = 0;

# Eerst de checkbox wegschrijven
#foreach (@checkboxes) {
#	my @checkboxContent = split /;/, $checkboxes[$currentArray];
#	$checkboxContent[1] =~ s/\[/&#60\;/g;
#	$checkboxContent[1] =~ s/\]/&#62\;/g;

#	$checkboxContent[0] =~ s/^\s+//;
#	$checkboxContent[0] =~ s/\s+$//;		
#	$checkboxContent[1] =~ s/^\s+//;
#	$checkboxContent[1] =~ s/\s+$//;		

#	print FILE4 "CHECKBOX: " . $checkboxContent[0] . " >> METADATANAAM: " . $metadataName[$metadataArray] . " / METADATAGUID: " . $metadataGUID[$metadataArray] . "\n";

#	print FILE2 "<Question id=\"CHKBOX_" . $currentArray . "\" name=\"\">\n";
#	print FILE2 "<!--RU_001-->\n";
#	print FILE2 "<Checkbox id=\"" . $checkboxContent[0] . "\" metadataID=\"" . $metadataGUID[$metadataArray++] . "\" metadataName=\"" . $metadataName[$currentArray++] . "\" label=\"" . $checkboxContent[1] . "\" />\n";
#	print FILE2 "</Question>\n";
#}

#print FILE2 "</Questions>\n";
#print FILE2 "</Step>\n";

# **************
# *** STAP 3 ***
# **************
print FILE2 "<Step id=\"2\" name=\"" . $baseFile . "\" groupName=\"Buitenland\" type=\"STEP\">\n";
print FILE2 "<Conditions>\n";
print FILE2 "<Condition nextStepID=\"4\">\n";
print FILE2 "<Equal>\n";
print FILE2 "<Control id=\"CHECKBOX_bijlage\" />\n";
print FILE2 "<Const val=\"False\" />\n";
print FILE2 "</Equal>\n";
print FILE2 "</Condition>\n";
print FILE2 "</Conditions>\n";
print FILE2 "<Questions>\n";


# Dan de velden wegschrijven
my $currentArray = 0;
foreach (@unique_matches) {
	print FILE4 "VELD: " . $unique_matches[$currentArray] . " >> METADATANAAM: " . $metadataName[$metadataArray] . " / METADATAGUID: " . $metadataGUID[$metadataArray] . "\n";
	print FILE2 "<!--RU_001-->\n";

	# Als het een checkbox betreft
	if (substr($unique_matches[$currentArray],0,8) eq "checkbox") {
		print "FOUND A CHECKBOX!!!\n";
		my @checkboxContent = split /;/, $unique_matches[$currentArray];
		$checkboxContent[1] =~ s/\[/&#60\;/g;
		$checkboxContent[1] =~ s/\]/&#62\;/g;

		$checkboxContent[0] =~ s/^\s+//;
		$checkboxContent[0] =~ s/\s+$//;		
		$checkboxContent[1] =~ s/^\s+//;
		$checkboxContent[1] =~ s/\s+$//;		

	# Een mooi lijntje trekken boven de checkbox
		print FILE2 "<Question id=\"CHKBOX_" . $currentArray . "\" name=\"\">\n";
		print FILE2 "<!--RU_001-->\n";
		print FILE2 "<Checkbox id=\"" . $checkboxContent[0] . "\" metadataID=\"" . $metadataGUID[$metadataArray++] . "\" metadataName=\"" . $metadataName[$currentArray] . "\" label=\"" . $checkboxContent[1] . "\" />\n";
		#print FILE2 "</Question>\n";
	}	

	# Als het een list-item betreft
	if (substr($unique_matches[$currentArray],0,4) eq "list") {
		# Stop de naam en de waarden in een array
		my @listitems = split /;/, $unique_matches[$currentArray];
		print FILE2 "<Question id=\"BTL_STR_002_1" . $currentArray . "\" name=\"" . substr($listitems[0],5) . "\">\n";
		print FILE2 "<List id=\"" . substr($listitems[0],5) . "\" metadataID=\"" . $metadataGUID[$metadataArray++] . "\" metadataName=\"" . $metadataName[$currentArray] . "\" required=\"true\">\n";
		shift @listitems;
		print FILE2 "<Items>\n";
		foreach (@listitems) {
			print FILE2 "<Item><Value>" . trim($_) . "</Value></Item>\n";
		}
		print FILE2 "</Items>\n";
		print FILE2 "</List>\n";
	} 
	
	# Een lijn tussen de vragen plaatsen
	if (substr($unique_matches[$currentArray],0,4) eq "line"){
		print FILE2 "<Question name=\"\" id=\"HORIZ_LINE_" . $currentArray . "\">\n";
		print FILE2 "<Label defaultValue=\"&#60;hr style=&#34;height: 1px; border: 0px solid #CCCCCC; border-top-width: 1px;&#34; /&#62;\" id=\"HORIZ_LINE_" . $currentArray . "\" />\n";
	}
	
	# Vraag stellen (als het geen "list", "checkbox" of "line" is)
	if (substr($unique_matches[$currentArray],0,4) ne "list" && substr($unique_matches[$currentArray],0,8) ne "checkbox" && substr($unique_matches[$currentArray],0,4) ne "line") {
		print FILE2 "<Question id=\"BTL_STR_002_1" . $currentArray . "\" name=\"" . $unique_matches[$currentArray] . "\">\n";
		print FILE2 "<String id=\"" . $unique_matches[$currentArray] . "\" metadataID=\"" . $metadataGUID[$metadataArray++] . "\" metadataName=\"" . $metadataName[$currentArray] . "\"/>\n";
	}
	print FILE2 "</Question>\n";
	$currentArray++;
}

# And lastly the footer of the XML
print FILE2 "<Question id=\"SPECIFIEK\" name=\"Bijlage(n) uploaden?\">\n";
print FILE2 "<Checkbox id=\"CHECKBOX_bijlage\" defaultValue=\"" . $defaultbijlageuploaden . "\"></Checkbox>\n";
print FILE2 "</Question>\n";
print FILE2 "</Questions>\n";
print FILE2 "</Step>\n";

# **************
# *** STAP 4 ***
# **************
print FILE2 "<Step id=\"3\" name=\"BIJLAGE\" groupName=\"Buitenland\" type=\"STEP\">\n";
print FILE2 "<Questions>\n";
print FILE2 "<Question id=\"BTLBL_001\" name=\"\">\n";
print FILE2 "<!--RU_005-->\n";
print FILE2 "<Label defaultValue=\"Bijlage 1 t/m 5 omschrijving, bestand (PDF)\" id=\"BTLBL_001_1\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_001\" name=\"\">\n";
print FILE2 "<!--RU_006-->\n";
print FILE2 "<Multi id=\"BTLOMS_001_1\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"BTLOMS_001_1_1\" metadataID=\"ecdf1362-4759-4d0a-8269-8e383b4a5cc4\" metadataName=\"bijlage_oms_01\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_001_2\" name=\"\">\n";
print FILE2 "<!--RU_009-->\n";
print FILE2 "<Attachment id=\"BTLOMS_001_2_1\" metadataID=\"8650af49-ebe3-4167-9a52-2d8b0ead907c\" metadataName=\"bijlage_code_01\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_002\" name=\"\">\n";
print FILE2 "<!--RU_007-->\n";
print FILE2 "<Multi id=\"BTLOMS_002_1\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"BTLOMS_002_1_1\" metadataID=\"1979af9a-cf61-490f-a69e-84127f1b9b74\" metadataName=\"bijlage_oms_02\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_002_2\" name=\"\">\n";
print FILE2 "<!--RU_010-->\n";
print FILE2 "<Attachment id=\"BTLOMS_002_2_1\" metadataID=\"af9395f6-ad6a-4f2d-9a03-742a514094b1\" metadataName=\"bijlage_code_02\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_003\" name=\"\">\n";
print FILE2 "<!--RU_008-->\n";
print FILE2 "<Multi id=\"BTLOMS_003_1\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"BTLOMS_003_1_1\" metadataID=\"2befd6ad-e02d-43ad-8efb-f55ae57d46ac\" metadataName=\"bijlage_oms_03\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_003_2\" name=\"\">\n";
print FILE2 "<!--RU_011-->\n";
print FILE2 "<Attachment id=\"BTLOMS_003_2_1\" metadataID=\"c91d6a9a-25ee-408e-a624-494bc314c067\" metadataName=\"bijlage_code_03\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_004\" name=\"\">\n";
print FILE2 "<!--RU_008-->\n";
print FILE2 "<Multi id=\"BTLOMS_004_1\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"BTLOMS_004_1_1\" metadataID=\"511e23ac-e08f-4148-84ec-6b75b8d50bd5\" metadataName=\"bijlage_oms_04\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_004_2\" name=\"\">\n";
print FILE2 "<!--RU_011-->\n";
print FILE2 "<Attachment id=\"BTLOMS_004_2_1\" metadataID=\"96b9e403-c69d-4643-9c92-a7cc46f9a2ea\" metadataName=\"bijlage_code_04\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_005\" name=\"\">\n";
print FILE2 "<!--RU_008-->\n";
print FILE2 "<Multi id=\"BTLOMS_005_1\">\n";
print FILE2 "<Controls>\n";
print FILE2 "<String id=\"BTLOMS_005_1_1\" metadataID=\"aeaed936-9b64-4adc-b8c1-14379f031891\" metadataName=\"bijlage_oms_05\"/>\n";
print FILE2 "</Controls>\n";
print FILE2 "</Multi>\n";
print FILE2 "</Question>\n";
print FILE2 "<Question id=\"BTLOMS_005_2\" name=\"\">\n";
print FILE2 "<!--RU_011-->\n";
print FILE2 "<Attachment id=\"BTLOMS_005_2_1\" metadataID=\"efd8aa89-a1a9-4a73-8c9f-6989237c725a\" metadataName=\"bijlage_code_05\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "</Questions>\n";
print FILE2 "</Step>\n";
print FILE2 "<Step id=\"4\" name=\"EINDE\" groupName=\"BUITENLAND\" type=\"FINISH\">\n";
print FILE2 "<Questions>\n";
print FILE2 "<Question id=\"FINISCH\" name=\"\">\n";
print FILE2 "<Label id=\"FINISCH_1\" defaultValue=\"Het document is klaar\"/>\n";
print FILE2 "</Question>\n";
print FILE2 "</Questions>\n";
print FILE2 "</Step>\n";
print FILE2 "</Steps>\n";
print FILE2 "</Wizard>\n";

close FILE;
close FILE2;
close FILE4;

}
