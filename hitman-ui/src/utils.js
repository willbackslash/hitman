export const hasHitmenPermissions = (profile) => profile && (profile.roles.includes('manager') || profile.is_superuser);
export const canAssignHits = (profile) => profile && (profile.roles.includes('manager') || profile.is_superuser);
export const isHitman = (user) => Array.from(user.roles, (role) => role.name).includes('hitman');
export const isManager = (user) => Array.from(user.roles, (role) => role.name).includes('manager');
export const isBoss = (user) => user.is_superuser;

export default {
  hasHitmenPermissions,
  canAssignHits,
  isHitman,
  isManager,
  isBoss,
};
