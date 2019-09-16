function set_or_validate_session(is_lti_launch,
                                 lti_session_key) {
    
    sessionStorage.setItem('lti_session_key', lti_session_key);

}
