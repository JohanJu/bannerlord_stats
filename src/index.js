import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import TableFilter from 'react-table-filter';
import "react-table-filter/lib/styles.css";
import data from './data.json';
import { } from './example.scss';

const keys = ['id', 'group', 'lvl', 'culture',
  'Item0', 'Item1', 'Item2', 'Item3', 'Head', 'Cape', 'Body', 'Gloves', 'Leg',
  'Athletics', 'Riding', 'OneHanded', 'TwoHanded', 'Polearm', 'Bow', 'Crossbow', 'Throwing',
  'horse', 'harness'
]

const nof = ['Item0', 'Item1', 'Item2', 'Item3', 'Head', 'Cape', 'Body', 'Gloves', 'Leg', 'horse', 'harness']

class SimpleExample extends Component {
  constructor(props) {
    super(props);
    this.state = {
      'episodes': data,
    };
    this._filterUpdated = this._filterUpdated.bind(this);
  }

  _filterUpdated(newData, filtersObject) {
    this.setState({
      'episodes': newData,
    });
  }

  render() {
    const chars = this.state.episodes;
    let c2 = []
    let tr = []
    for (let i = 0; i < chars.length; i++) {
      let td = []
      let cc2 = Object.assign({}, chars[i])
      for (let j = 0; j < keys.length; j++) {
        let elm = chars[i][keys[j]]
        if (elm instanceof Object) {
          elm = <div class="tooltip">{elm.text}
            <span class="tooltiptext">{elm.tip}</span>
          </div>
        }
        td.push(<td className="cell">{elm}</td>)
        if (cc2[keys[j]] instanceof Object) {
          cc2[keys[j]] = cc2[keys[j]].text
        }
      }
      c2.push(cc2)
      tr.push(<tr>{td}</tr>)
    }
    let th = []
    for (let i = 0; i < keys.length; i++) {
      if (nof.includes(keys[i])) {
        th.push(<th key={keys[i]} className={keys[i]}>{keys[i]}</th>)
      } else {
        th.push(<th key={keys[i]} filterkey={keys[i]} className={keys[i]}>{keys[i]}</th>)
      }
    }
    return (
      <div>
        <table className="basic-table">
          <thead>
            <TableFilter
              rows={chars}
              onFilterUpdate={this._filterUpdated}>
              {th}
            </TableFilter>
          </thead>
          <tbody>
            {tr}
          </tbody>
        </table>
      </div>
    );
  }
}

ReactDOM.render(
  [<div> v1.1.0</div >,
  <a href={'https://github.com/JohanJu/bannerlord_stats'}>Github</a>,
  <SimpleExample />],
  document.getElementById('root')
);