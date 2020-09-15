export const hasHitmenPermissions = (profile) => profile && (profile.roles.includes('manager') || profile.is_super_user);

export default {
  hasHitmenPermissions,
};
