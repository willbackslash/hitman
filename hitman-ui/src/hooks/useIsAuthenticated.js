const useIsAuthenticaded = () => sessionStorage.getItem('SESSION_AUTH') != null;

export default useIsAuthenticaded;
