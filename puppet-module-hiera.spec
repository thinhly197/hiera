Name            : puppet-module-hiera
Summary         : Puppet Wemall Module and Hiera
Version         : %{?version}%{!?version:1.0.0}
Release         : %{?release}%{!?release:0}

Group           : Applications/File
License         : (c)Douglas Gibbons

BuildArch       : %{?arch}%{!?arch:x86_64}
BuildRoot       : %{_tmppath}/%{name}-%{version}-root


# Use "Requires" for any dependencies, for example:
# Requires        : httpd

# Description gives information about the rpm package. This can be expanded up to multiple lines.
%description
"Wemall" source code


# Prep is used to set up the environment for building the rpm package
# Expansion of source tar balls are done in this section
%prep

# Used to compile and to build the source
%build

%pre
if [ "$1" = "1" ]; then
  echo "pre ==> for new install"
elif [ "$1" = "2" ]; then
  echo "pre ==> for upgrade"
  rm -rf /data/puppet/common
fi

# The installation.
# We actually just put all our install files into a directory structure that mimics a server directory structure here
%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/data/puppet/common
cp ../SOURCES/*.tar.gz $RPM_BUILD_ROOT/data/puppet/common

# Contains a list of the files that are part of the package
# See useful directives such as attr here: http://www.rpm.org/max-rpm-snapshot/s1-rpm-specref-files-list-directives.html
%files
#%defattr(0644, apache, apache, 0755)
%dir %attr(0755, root, root) /data/puppet/common
%dir /data/puppet/common
/data/puppet/common/*.tar.gz

%post
#if [ "$1" = "1" ]; then
  echo "post ==> for new install"
  tar xfz /data/puppet/common/puppet-module-hiera-*.tar.gz -C /data/puppet/common/
  rm -rf /data/puppet/common/puppet-module-hiera-*.tar.gz
  ln -f -s /data/puppet/common/hiera/alpha/hieradata/ /etc/puppetlabs/puppet/hieradata
  ln -f -s /data/puppet/common/hiera/alpha/hiera.yaml /etc/puppetlabs/puppet/hiera.yaml
  ln -f -s /data/puppet/common/module/common/modules/ /etc/puppetlabs/puppet/modules
  #elif [ "$1" = "2" ]; then
#  echo "post ==> for upgrade"
#fi

%preun
if [ "$1" = "1" ]; then
  echo "preun ==> for upgrade"
elif [ "$1" = "0" ]; then
  echo "preun ==> for uninstall"
  rm -rf /data/puppet/common
  rm -f /data/puppet/common/*.tar.gz
fi

%postun
if [ "$1" = "1" ]; then
  echo "postun ==> for upgrade"
elif [ "$1" = "0" ]; then
  echo "postun ==> for uninstall"
fi

# Used to store any changes between versions
%changelog
