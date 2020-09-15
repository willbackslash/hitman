const useCanViewHitmen = (profile) => profile && (profile.roles.includes('manager') || profile.is_super_user);

export default useCanViewHitmen;
