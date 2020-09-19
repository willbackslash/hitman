export const hasHitmenPermissions = (profile) => profile && (profile.roles.includes('manager') || profile.is_super_user);
export const canAssignHits = (profile) => profile && (profile.roles.includes('manager') || profile.is_super_user);
export const isHitman = (user) => Array.from(user.roles, (role) => role.name).includes('hitman');
export const isManager = (user) => Array.from(user.roles, (role) => role.name).includes('manager');
export const isBoss = (user) => user.is_super_user || user.is_superuser;

export default {
  hasHitmenPermissions,
  canAssignHits,
  isHitman,
  isManager,
  isBoss,
};
