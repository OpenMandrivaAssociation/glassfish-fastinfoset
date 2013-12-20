%_javapackages_macros
Name:          glassfish-fastinfoset
Version:       1.2.12
Release:       9.0%{?dist}
Summary:       Fast Infoset
License:       ASL 2.0
URL:           https://fi.dev.java.net
# svn export https://svn.java.net/svn/fi~svn/tags/1_2_12/ glassfish-fastinfoset-1.2.12
# find glassfish-fastinfoset-1.2.12/ -name '*.class' -delete
# find glassfish-fastinfoset-1.2.12/ -name '*.jar' -delete
# rm -rf glassfish-fastinfoset-1.2.12/roundtrip-tests
# tar czf glassfish-fastinfoset-1.2.12-src-svn.tar.gz glassfish-fastinfoset-1.2.12
Source0:       %{name}-%{version}-src-svn.tar.gz
# add xmlstreambuffer 1.5.x support
Patch0:        %{name}-%{version}-utilities-FastInfosetWriterSAXBufferProcessor.patch

BuildRequires: bea-stax-api
BuildRequires: maven-local
BuildRequires: maven-plugin-jxr
BuildRequires: maven-plugin-tools-api
BuildRequires: maven-project-info-reports-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-source-plugin
BuildRequires: xsom
BuildRequires: maven-surefire-provider-junit4
BuildRequires: jvnet-parent
BuildRequires: xmlstreambuffer

BuildArch:     noarch

%description
Fast Infoset specifies a standardized binary encoding for the XML Information
Set. An XML infoset (such as a DOM tree, StAX events or SAX events in
programmatic representations) may be serialized to an XML 1.x document or, as
specified by the Fast Infoset standard, may be serialized to a fast infoset
document.  Fast infoset documents are generally smaller in size and faster to
parse and serialize than equivalent XML documents.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0
# Remove wagon-webdav
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-antrun-extended-plugin

# Replace javax.xml.bind jsr173_api with stax (bea-)stax-api
%pom_remove_dep javax.xml.bind:jsr173_api
%pom_add_dep stax:stax-api:1.0.1

%pom_disable_module roundtrip-tests
%pom_disable_module samples

%build

%mvn_file :FastInfoset %{name}
%mvn_file :FastInfosetUtilities %{name}-utilities
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc
