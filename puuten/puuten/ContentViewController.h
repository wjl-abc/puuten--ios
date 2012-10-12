//
//  ContentViewController.h
//  puuten
//
//  Created by wang jialei on 12-10-6.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface ContentViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    NSMutableArray *array4wb;
    NSMutableDictionary *dicData;
    NSMutableDictionary *dic4wb;
    WaterFlowView  *waterFlow;
    int selected_cell;
    int selected_order;
}
@property (assign, nonatomic) NSString *categ;
@property (assign, nonatomic) NSString *type;
- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end