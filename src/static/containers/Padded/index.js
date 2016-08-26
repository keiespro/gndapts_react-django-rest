import React from 'react';
import { connect } from 'react-redux';
import './style.scss';


class PaddedContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    static propTypes = {
        children: React.PropTypes.element.isRequired,
    };

    render() {
        return (
            <div id="padded-container">
                {this.props.children}
            </div>
        )
    }

}

export default connect()(PaddedContainer);
export { PaddedContainer as PaddedHolderNotConnected };

