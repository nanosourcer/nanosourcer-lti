#!/usr/bin/perl

my @files = `cat files.txt`;
for $line (@files) {
    chomp $line;
    $xmlfile = "$line.xml";
    $jpgfile = "$line.jpg";
    $template = <<_END;
queue:
	-\@rm -rf /tmp/test
	-\@mkdir /tmp/test
	cp $jpgfile /tmp/test
	cp $xmlfile /tmp/test
drush \\
	--user=admin \\
	--uri=http://default \\
	islandora_batch_scan_preprocess \\
	--content_models=islandora:sp_basic_image \\
	--parent=islandora:20 \\
	--parent_relationship_pred=isMemberOfCollection \\
	--type=directory \\
	--target=/tmp/test
ingest:
	drush \\
	--user=admin \\
	--uri=http://default \\
	islandora_batch_ingest
_END

    open(my $OT, ">", "Makefile");
    print $OT  $template;
    close $OT;

    print `make`;

}


