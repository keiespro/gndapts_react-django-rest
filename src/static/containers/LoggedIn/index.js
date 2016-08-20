import React from 'react';
import { connect } from 'react-redux';
import './style.scss';
import { authLogoutAndRedirect } from '../../actions/auth';
import { Link } from 'react-router';
import { push } from 'react-router-redux';

class LoggedInView extends React.Component {

    static propTypes = {
        isAuthenticated: React.PropTypes.bool.isRequired,
        children: React.PropTypes.object.isRequired,
        dispatch: React.PropTypes.func.isRequired,
        firstName: React.PropTypes.string.isRequired,
        pathName: React.PropTypes.string.isRequired
    };

    constructor(props) {
        super(props);

        this.state = {
        };
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    logout = () => {
        this.props.dispatch(authLogoutAndRedirect());
    };

    render() {
        return (
            <div>
                <div className="ui fixed menu">
                    <div className="ui container">
                        <a href="#" onClick={() => this.props.dispatch(push('/home'))} className="header item">
                            <img className="logo" src="http://semantic-ui.com/examples/assets/images/logo.png"/>
                            GNDAPTS
                        </a>
                        <a href="#" onClick={() => this.props.dispatch(push('/map'))} className="item">
                            <i className="fa fa-map-marker" aria-hidden="true"></i>&nbsp;Map
                        </a>
                        <div className="right menu">
                            <a href="#" className="right item">
                                Post
                            </a>
                            <a href="#" className="right item">
                                Post (LL)
                            </a>
                            <a href="#" className="right item">
                                Review
                            </a>
                            <div className="ui simple dropdown item">
                                {this.props.firstName} <i className="dropdown icon"></i>
                                <div className="menu">
                                    <a className="item" href="#" onClick={this.logout}>
                                        Logout
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="main">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        isAuthenticated: state.auth.isAuthenticated,
        firstName: state.auth.firstName,
        pathName: ownProps.location.pathname
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

export default connect(mapStateToProps)(LoggedInView);
export { LoggedInView as LoggedInNotConnected };