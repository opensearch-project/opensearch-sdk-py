from stream_input import StreamInput
from stream_output import StreamOutput

class DiscoveryNode:
    def __init__(self):
        super().__init__(self)

    def read_from(self, input: StreamInput):
        # this.nodeName = in.readString().intern();
        # this.nodeId = in.readString().intern();
        # this.ephemeralId = in.readString().intern();
        # this.hostName = in.readString().intern();
        # this.hostAddress = in.readString().intern();
        # this.address = new TransportAddress(in);
        # int size = in.readVInt();
        # this.attributes = new HashMap<>(size);
        # for (int i = 0; i < size; i++) {
        #     this.attributes.put(in.readString(), in.readString());
        # }
        # int rolesSize = in.readVInt();
        # final Set<DiscoveryNodeRole> roles = new HashSet<>(rolesSize);
        # for (int i = 0; i < rolesSize; i++) {
        #     final String roleName = in.readString();
        #     final String roleNameAbbreviation = in.readString();
        #     final boolean canContainData = in.readBoolean();
        #     final DiscoveryNodeRole role = roleMap.get(roleName);
        #     if (role == null) {
        #         if (in.getVersion().onOrAfter(Version.V_2_1_0)) {
        #             roles.add(new DiscoveryNodeRole.DynamicRole(roleName, roleNameAbbreviation, canContainData));
        #         } else {
        #             roles.add(new DiscoveryNodeRole.UnknownRole(roleName, roleNameAbbreviation, canContainData));
        #         }
        #     } else {
        #         assert roleName.equals(role.roleName()) : "role name [" + roleName + "] does not match role [" + role.roleName() + "]";
        #         assert roleNameAbbreviation.equals(role.roleNameAbbreviation()) : "role name abbreviation ["
        #             + roleName
        #             + "] does not match role ["
        #             + role.roleNameAbbreviation()
        #             + "]";
        #         roles.add(role);
        #     }
        # }
        # this.roles = Collections.unmodifiableSortedSet(new TreeSet<>(roles));
        # this.version = in.readVersion();
        pass

    def write_to(self, output: StreamOutput):
        pass
