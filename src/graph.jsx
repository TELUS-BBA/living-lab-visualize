import React from 'react';
import axios from 'axios';
import Paragraph from '@tds/core-paragraph';

class TopLevel extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
    axios.get('http://localhost:5001/nanopi/', {auth: {username: '', password: ''}})
      .then( response => {
        this.setState({data: response.data});
      })
      .catch( error => {
        console.log(error);
      });
  }

  render() {
    let data = this.state.data.map( element => (
      <div>
        <Paragraph>
          { element.id } and a lovely block of text!
        </Paragraph>
      </div>
    ));
    return (
      <div>
        { data }
        <Paragraph>
          Here's a paragraph!
        </Paragraph>
      </div>
    );
  }
}

export default TopLevel;
