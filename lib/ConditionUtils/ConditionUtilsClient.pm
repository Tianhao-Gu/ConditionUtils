package ConditionUtils::ConditionUtilsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

ConditionUtils::ConditionUtilsClient

=head1 DESCRIPTION


A KBase module: ConditionUtils


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => ConditionUtils::ConditionUtilsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 get_conditions

  $result = $obj->get_conditions($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a ConditionUtils.GetConditionParams
$result is a ConditionUtils.GetConditionOutput
GetConditionParams is a reference to a hash where the following keys are defined:
	condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
	conditions has a value which is a reference to a list where each element is a string
ws_condition_set_id is a string
GetConditionOutput is a reference to a hash where the following keys are defined:
	conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a hash where the key is a string and the value is a reference to a list where each element is a ConditionUtils.Factor
Factor is a reference to a hash where the following keys are defined:
	factor_label has a value which is a string
	factor_ont_ref has a value which is a string
	factor_ont_id has a value which is a string
	unit_id has a value which is a string
	unit_ont_id has a value which is a string
	value has a value which is a string

</pre>

=end html

=begin text

$params is a ConditionUtils.GetConditionParams
$result is a ConditionUtils.GetConditionOutput
GetConditionParams is a reference to a hash where the following keys are defined:
	condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
	conditions has a value which is a reference to a list where each element is a string
ws_condition_set_id is a string
GetConditionOutput is a reference to a hash where the following keys are defined:
	conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a hash where the key is a string and the value is a reference to a list where each element is a ConditionUtils.Factor
Factor is a reference to a hash where the following keys are defined:
	factor_label has a value which is a string
	factor_ont_ref has a value which is a string
	factor_ont_id has a value which is a string
	unit_id has a value which is a string
	unit_ont_id has a value which is a string
	value has a value which is a string


=end text

=item Description



=back

=cut

 sub get_conditions
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_conditions (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_conditions:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_conditions');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "ConditionUtils.get_conditions",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_conditions',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_conditions",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_conditions',
				       );
    }
}
 


=head2 file_to_condition_set

  $result = $obj->file_to_condition_set($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a ConditionUtils.FileToConditionSetParams
$result is a ConditionUtils.FileToConditionSetOutput
FileToConditionSetParams is a reference to a hash where the following keys are defined:
	input_shock_id has a value which is a string
	input_file_path has a value which is a string
	output_ws_name has a value which is a string
	output_obj_name has a value which is a string
FileToConditionSetOutput is a reference to a hash where the following keys are defined:
	output_condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string

</pre>

=end html

=begin text

$params is a ConditionUtils.FileToConditionSetParams
$result is a ConditionUtils.FileToConditionSetOutput
FileToConditionSetParams is a reference to a hash where the following keys are defined:
	input_shock_id has a value which is a string
	input_file_path has a value which is a string
	output_ws_name has a value which is a string
	output_obj_name has a value which is a string
FileToConditionSetOutput is a reference to a hash where the following keys are defined:
	output_condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string


=end text

=item Description



=back

=cut

 sub file_to_condition_set
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function file_to_condition_set (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to file_to_condition_set:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'file_to_condition_set');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "ConditionUtils.file_to_condition_set",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'file_to_condition_set',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method file_to_condition_set",
					    status_line => $self->{client}->status_line,
					    method_name => 'file_to_condition_set',
				       );
    }
}
 


=head2 condition_set_to_tsv_file

  $result = $obj->condition_set_to_tsv_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a ConditionUtils.ConditionSetToTsvFileParams
$result is a ConditionUtils.ConditionSetToTsvFileOutput
ConditionSetToTsvFileParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
	destination_dir has a value which is a string
ws_condition_set_id is a string
ConditionSetToTsvFileOutput is a reference to a hash where the following keys are defined:
	file_path has a value which is a string

</pre>

=end html

=begin text

$params is a ConditionUtils.ConditionSetToTsvFileParams
$result is a ConditionUtils.ConditionSetToTsvFileOutput
ConditionSetToTsvFileParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
	destination_dir has a value which is a string
ws_condition_set_id is a string
ConditionSetToTsvFileOutput is a reference to a hash where the following keys are defined:
	file_path has a value which is a string


=end text

=item Description



=back

=cut

 sub condition_set_to_tsv_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function condition_set_to_tsv_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to condition_set_to_tsv_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'condition_set_to_tsv_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "ConditionUtils.condition_set_to_tsv_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'condition_set_to_tsv_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method condition_set_to_tsv_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'condition_set_to_tsv_file',
				       );
    }
}
 


=head2 export_condition_set_tsv

  $result = $obj->export_condition_set_tsv($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a ConditionUtils.ExportConditionSetParams
$result is a ConditionUtils.ExportConditionSetOutput
ExportConditionSetParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string
ExportConditionSetOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string

</pre>

=end html

=begin text

$params is a ConditionUtils.ExportConditionSetParams
$result is a ConditionUtils.ExportConditionSetOutput
ExportConditionSetParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string
ExportConditionSetOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string


=end text

=item Description



=back

=cut

 sub export_condition_set_tsv
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function export_condition_set_tsv (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to export_condition_set_tsv:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'export_condition_set_tsv');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "ConditionUtils.export_condition_set_tsv",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'export_condition_set_tsv',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method export_condition_set_tsv",
					    status_line => $self->{client}->status_line,
					    method_name => 'export_condition_set_tsv',
				       );
    }
}
 


=head2 export_condition_set_excel

  $result = $obj->export_condition_set_excel($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a ConditionUtils.ExportConditionSetParams
$result is a ConditionUtils.ExportConditionSetOutput
ExportConditionSetParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string
ExportConditionSetOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string

</pre>

=end html

=begin text

$params is a ConditionUtils.ExportConditionSetParams
$result is a ConditionUtils.ExportConditionSetOutput
ExportConditionSetParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a ConditionUtils.ws_condition_set_id
ws_condition_set_id is a string
ExportConditionSetOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string


=end text

=item Description



=back

=cut

 sub export_condition_set_excel
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function export_condition_set_excel (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to export_condition_set_excel:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'export_condition_set_excel');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "ConditionUtils.export_condition_set_excel",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'export_condition_set_excel',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method export_condition_set_excel",
					    status_line => $self->{client}->status_line,
					    method_name => 'export_condition_set_excel',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "ConditionUtils.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "ConditionUtils.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'export_condition_set_excel',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method export_condition_set_excel",
            status_line => $self->{client}->status_line,
            method_name => 'export_condition_set_excel',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for ConditionUtils::ConditionUtilsClient\n";
    }
    if ($sMajor == 0) {
        warn "ConditionUtils::ConditionUtilsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 bool

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 Factor

=over 4



=item Description

Internally this is used to store factor information (without the value term) and also a
format for returning data in a useful form from get_conditions
@optional unit_id unit_ont_id value


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
factor_label has a value which is a string
factor_ont_ref has a value which is a string
factor_ont_id has a value which is a string
unit_id has a value which is a string
unit_ont_id has a value which is a string
value has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
factor_label has a value which is a string
factor_ont_ref has a value which is a string
factor_ont_id has a value which is a string
unit_id has a value which is a string
unit_ont_id has a value which is a string
value has a value which is a string


=end text

=back



=head2 ConditionSet

=over 4



=item Description

factors - list of supplied factors
conditions - mapping of condition_labels to a list of factor values in the same order as the factors array
Ontology_mapping_method - One of ???User curation???, ???Closest matching string???


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a list where each element is a string
factors has a value which is a reference to a list where each element is a ConditionUtils.Factor
ontology_mapping_method has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a list where each element is a string
factors has a value which is a reference to a list where each element is a ConditionUtils.Factor
ontology_mapping_method has a value which is a string


=end text

=back



=head2 ws_condition_set_id

=over 4



=item Description

@id ws ConditionSet


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 GetConditionParams

=over 4



=item Description

Get condition information in a friendly format

ws_condition_set_id condition_set_ref
list<string> conditions - Optional: Which conditions should be returned. defaults to all conditions in the set

Returns {condition_label: {ontology_type(e.g. GO): [Factors]}}


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
conditions has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id
conditions has a value which is a reference to a list where each element is a string


=end text

=back



=head2 GetConditionOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a hash where the key is a string and the value is a reference to a list where each element is a ConditionUtils.Factor

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
conditions has a value which is a reference to a hash where the key is a string and the value is a reference to a hash where the key is a string and the value is a reference to a list where each element is a ConditionUtils.Factor


=end text

=back



=head2 FileToConditionSetParams

=over 4



=item Description

input_shock_id and input_file_path - alternative input params,


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_shock_id has a value which is a string
input_file_path has a value which is a string
output_ws_name has a value which is a string
output_obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_shock_id has a value which is a string
input_file_path has a value which is a string
output_ws_name has a value which is a string
output_obj_name has a value which is a string


=end text

=back



=head2 FileToConditionSetOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
output_condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
output_condition_set_ref has a value which is a ConditionUtils.ws_condition_set_id


=end text

=back



=head2 ConditionSetToTsvFileParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_ref has a value which is a ConditionUtils.ws_condition_set_id
destination_dir has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_ref has a value which is a ConditionUtils.ws_condition_set_id
destination_dir has a value which is a string


=end text

=back



=head2 ConditionSetToTsvFileOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
file_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
file_path has a value which is a string


=end text

=back



=head2 ExportConditionSetParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_ref has a value which is a ConditionUtils.ws_condition_set_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_ref has a value which is a ConditionUtils.ws_condition_set_id


=end text

=back



=head2 ExportConditionSetOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
shock_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
shock_id has a value which is a string


=end text

=back



=cut

package ConditionUtils::ConditionUtilsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
