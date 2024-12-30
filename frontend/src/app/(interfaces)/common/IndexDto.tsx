import { Group } from "./Group";
import { Mapping } from "./Mapping";
import { Topolgy } from "./Topology";

export interface IndexDto {
  topologies: Topolgy[];
  groups: Group[];
  mappings: Mapping[]
}